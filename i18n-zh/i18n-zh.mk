# =============================================================================
# EVO Player 简体中文补丁 - Makefile 片段
#
# 用法：在 projects/evoplayer/Makefile 里加一行
#
#     include i18n-zh/i18n-zh.mk
#
# 位置必须在 `C_SRCS := ...` 之后、`C_OBJS := $(C_SRCS:.c=.o)` 之前，
# 否则 i18n-zh/src/evo_i18n.o 不会进 C_OBJS，链接时会缺符号。
# tools/install.py 会自动插到正确位置。
# =============================================================================

I18N_ZH_DIR  := i18n-zh
I18N_ZH_SRCS := $(I18N_ZH_DIR)/src/evo_i18n.c

# evo_i18n.h 在这个目录里；C 和 C++ 都要能找到
CFLAGS   += -I$(I18N_ZH_DIR)/include
CXXFLAGS += -I$(I18N_ZH_DIR)/include

C_SRCS += $(I18N_ZH_SRCS)
