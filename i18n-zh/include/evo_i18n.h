/*
 * evo_i18n.h - EVO Player 的界面文本翻译入口（简体中文补丁）。
 *
 * 用法：把要显示的英文 UI 字面量交给 evo_tr()，返回当前语言的文案；表里没有
 * 时原样返回英文，所以未翻译的句子不会变成空白。
 *
 *   ui::text(list, font, evo_tr("VIDEO & DISPLAY"), ...);
 *
 * 两套词表：
 *   1. 编译进二进制的内置表（core/src/i18n/evo_i18n_table.inc，由 zh-CN.tsv 生成）
 *   2. 运行时覆盖 /data/evoplayer/lang/zh-CN.tsv（格式：英文<TAB>中文）
 * 覆盖表优先，改一句译文不必重新编译。
 */
#ifndef EVO_I18N_H
#define EVO_I18N_H

#ifdef __cplusplus
extern "C" {
#endif

/* 返回 en 的中文译文；没有译文或 en 为 NULL 时原样返回 en。 */
const char *evo_tr(const char *en);

/*
 * 载入运行时词表。path 为 NULL 时只使用内置表。
 * 不调用也可以：首次调用 evo_tr() 会自动尝试
 * /data/evoplayer/lang/zh-CN.tsv。
 * 返回载入的条目数（-1 表示文件打不开）。
 */
int evo_i18n_load(const char *path);

/* 内置表非空即返回 1。 */
int evo_i18n_enabled(void);

#ifdef __cplusplus
}
#endif

#endif /* EVO_I18N_H */
