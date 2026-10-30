/*
 * evo_i18n.c - 内置中文词表 + 运行时覆盖词表。
 *
 * 纯 C11，不依赖 C++ 或项目内部头文件，方便被 core/、addons/（.c）和
 * ui_kit/（.cpp）同时调用。
 *
 * 词表由 tools/gen_table.py 从 zh-CN.tsv 生成，不要手改 include 文件。
 */
#include "evo_i18n.h"

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    const char *en;
    const char *zh;
} EvoTrEntry;

/* 由 zh-CN.tsv 生成：{"英文", "中文"}, 每行一条。 */
static const EvoTrEntry kTable[] = {
#include "evo_i18n_table.inc"
};

#define EVO_TR_TABLE_COUNT (sizeof(kTable) / sizeof(kTable[0]))
#define EVO_TR_SLOTS 4096u          /* > 2 × 词条数，线性探测足够 */
#define EVO_TR_OV_SLOTS 2048u

typedef struct
{
    char *en;
    char *zh;
} EvoTrOverride;

static unsigned short g_index[EVO_TR_SLOTS];   /* 内置表下标 + 1 */
static EvoTrOverride *g_ov;
static int g_ov_count;
static int g_ov_cap;
static unsigned short g_ov_index[EVO_TR_OV_SLOTS];
static int g_ready;
static int g_loaded;
static pthread_once_t g_once = PTHREAD_ONCE_INIT;

/* FNV-1a，和词表生成脚本里的哈希一致，仅用于定位槽位。 */
static unsigned int evo_hash(const char *s)
{
    unsigned int h = 2166136261u;
    while (*s)
    {
        h ^= (unsigned char)*s++;
        h *= 16777619u;
    }
    return h;
}

static void evo_build_index(void)
{
    for (size_t i = 0; i < EVO_TR_TABLE_COUNT; ++i)
    {
        unsigned int slot = evo_hash(kTable[i].en) & (EVO_TR_SLOTS - 1u);
        while (g_index[slot])
            slot = (slot + 1u) & (EVO_TR_SLOTS - 1u);
        g_index[slot] = (unsigned short)(i + 1u);
    }
}

/* 把一行 "英文<TAB>中文" 存进覆盖表；返回 0 表示这一行无效或内存不足。 */
static int evo_ov_add(const char *en, size_t en_len, const char *zh, size_t zh_len)
{
    if (g_ov_count == g_ov_cap)
    {
        int cap = g_ov_cap ? g_ov_cap * 2 : 64;
        EvoTrOverride *p = (EvoTrOverride *)realloc(g_ov, sizeof(EvoTrOverride) * (size_t)cap);
        if (!p)
            return 0;
        g_ov = p;
        g_ov_cap = cap;
    }
    char *e = (char *)malloc(en_len + 1);
    char *z = (char *)malloc(zh_len + 1);
    if (!e || !z)
    {
        free(e);
        free(z);
        return 0;
    }
    memcpy(e, en, en_len);
    e[en_len] = '\0';
    memcpy(z, zh, zh_len);
    z[zh_len] = '\0';

    unsigned int slot = evo_hash(e) & (EVO_TR_OV_SLOTS - 1u);
    while (g_ov_index[slot])
        slot = (slot + 1u) & (EVO_TR_OV_SLOTS - 1u);
    g_ov_index[slot] = (unsigned short)(g_ov_count + 1);

    g_ov[g_ov_count].en = e;
    g_ov[g_ov_count].zh = z;
    ++g_ov_count;
    return 1;
}

static int evo_load_tsv(const char *path)
{
    FILE *f = fopen(path, "rb");
    if (!f)
        return -1;

    char line[4096];
    int added = 0;
    while (fgets(line, sizeof(line), f))
    {
        if (g_ov_count >= (int)EVO_TR_OV_SLOTS - 1)   /* 槽位满就停，避免死循环 */
            break;
        char *nl = line;
        while (*nl)
        {
            if (*nl == '\r' || *nl == '\n')
            {
                *nl = '\0';
                break;
            }
            ++nl;
        }
        if (line[0] == '\0' || line[0] == '#')
            continue;
        char *tab = strchr(line, '\t');
        if (!tab || tab == line)
            continue;
        *tab = '\0';
        if (evo_ov_add(line, strlen(line), tab + 1, strlen(tab + 1)))
            ++added;
    }
    fclose(f);
    return added;
}

static void evo_init_once(void)
{
    evo_build_index();
    /* 覆盖表是可选的：没有文件就只用内置表。 */
    evo_load_tsv("/data/evoplayer/lang/zh-CN.tsv");
    g_ready = 1;
}

int evo_i18n_load(const char *path)
{
    pthread_once(&g_once, evo_init_once);
    if (!path)
    {
        g_loaded = 0;
        return 0;
    }
    /* 先清空旧覆盖表，再载入新文件。 */
    for (int i = 0; i < g_ov_count; ++i)
    {
        free(g_ov[i].en);
        free(g_ov[i].zh);
    }
    g_ov_count = 0;
    memset(g_ov_index, 0, sizeof(g_ov_index));
    int n = evo_load_tsv(path);
    g_loaded = n > 0 ? 1 : 0;
    return n;
}

int evo_i18n_enabled(void)
{
    pthread_once(&g_once, evo_init_once);
    return EVO_TR_TABLE_COUNT > 0 ? 1 : 0;
}

const char *evo_tr(const char *en)
{
    if (!en)
        return NULL;
    pthread_once(&g_once, evo_init_once);
    (void)g_ready;

    const unsigned int h = evo_hash(en);

    /* 运行时覆盖优先。 */
    if (g_ov_count > 0)
    {
        unsigned int slot = h & (EVO_TR_OV_SLOTS - 1u);
        while (g_ov_index[slot])
        {
            const EvoTrOverride *o = &g_ov[g_ov_index[slot] - 1];
            if (strcmp(o->en, en) == 0)
                return o->zh;
            slot = (slot + 1u) & (EVO_TR_OV_SLOTS - 1u);
        }
    }

    unsigned int slot = h & (EVO_TR_SLOTS - 1u);
    while (g_index[slot])
    {
        const EvoTrEntry *e = &kTable[g_index[slot] - 1];
        if (strcmp(e->en, en) == 0)
            return e->zh;
        slot = (slot + 1u) & (EVO_TR_SLOTS - 1u);
    }
    return en;
}
