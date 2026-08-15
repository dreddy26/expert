{
  "meta": {
    "product": "OpenAkita Persona File Editor",
    "app_type": "developer_tool",
    "language": "ru-RU (UI тексты на русском; English technical terms не переводить)",
    "hard_bans": {
      "emoji": "Запрещены везде: UI, тексты, статусы, иконки. Разрешены только текстовые маркеры статуса: [OK], [RISK], [BLOCKER], [UNKNOWN], [FAIL], [PASS].",
      "decorative_pictographs": "Запрещены любые декоративные пиктограммы/иллюстрации. Только функциональные элементы.",
      "filler_copy": "Запрещены расплывчатые формулировки и 'вода'. Тексты короткие, измеримые, с числами."
    },
    "design_goal": "Максимальная информационная плотность: без второго скролла пользователь видит валидность файла, число провалов, и что реально уходит в system prompt (включая token cost двумя оценщиками).",
    "non_mocking_rule": "Любые числа/статусы в UI должны быть фактическими (из реального валидатора), не симулированными."
  },

  "inspiration_refs": {
    "layout_patterns": [
      {
        "name": "shadcn blocks — AI Code Editor",
        "url": "https://www.shadcn.io/blocks/ai-code-editor",
        "takeaways": [
          "IDE-подобная компоновка: панель кода + диагностика + статус-бар",
          "Плотные панели, четкие разделители, минимум декора"
        ]
      },
      {
        "name": "Lintscope — multi-linter dashboard",
        "url": "https://github.com/aggmoulik/lintscope",
        "takeaways": [
          "Виртуализированный список диагностик (масштаб до десятков тысяч)",
          "Триаж: фильтры, группировка, быстрый скролл"
        ]
      },
      {
        "name": "Deslint — report metrics",
        "url": "https://deslint.com/docs/getting-started",
        "takeaways": [
          "Метрики/сводка сверху: score, counts, fail threshold",
          "Экспортируемые отчеты и строгие fail-режимы"
        ]
      }
    ],
    "palette_refs": [
      {
        "name": "Liminal Salt Theme (WCAG-oriented)",
        "url": "https://github.com/irvj/liminal-salt-theme",
        "use": "База для нейтральных поверхностей + teal accent + amber warning + success/error"
      },
      {
        "name": "KonexForge Themes (role palette + WCAG claims)",
        "url": "https://marketplace.visualstudio.com/items?itemName=KonexForge.konexforge-themes",
        "use": "Референс для slate/graphite поверхностей и контрастных текстов"
      }
    ]
  },

  "brand_attributes": {
    "tone": ["строгий", "инженерный", "проверяемый", "без украшательств"],
    "visual_personality": ["IDE-like", "audit-grade", "dense", "high-contrast"],
    "motion_personality": ["быстро", "коротко", "без bounce", "без параллакса"]
  },

  "design_tokens": {
    "color_system": {
      "mode": "single (light by default) + optional dark toggle later; все поверхности имеют явный background",
      "palette_hex": {
        "bg": "#F5F2ED",
        "surface": "#FFFFFF",
        "surface_2": "#FBFAF7",
        "border": "#DDD8D0",
        "text": "#2D2B28",
        "text_muted": "#6B6761",
        "text_faint": "#9E9B93",

        "accent": "#506E58",
        "accent_2": "#3E5D5D",

        "ok": "#3A7346",
        "warn": "#7D6325",
        "fail": "#A54D4D",
        "info": "#2F5F73",

        "focus_ring": "#3E5D5D",

        "code_bg": "#0F1115",
        "code_text": "#E4E1DC",
        "code_border": "#2A2F37",
        "code_selection": "#243041",

        "badge_ok_bg": "#E7F3EA",
        "badge_warn_bg": "#F4EBDD",
        "badge_fail_bg": "#F6E6E6",
        "badge_info_bg": "#E6EFF3"
      },
      "semantic_roles": {
        "background": "bg",
        "card": "surface",
        "card_subtle": "surface_2",
        "border": "border",
        "foreground": "text",
        "muted_foreground": "text_muted",
        "primary": "accent",
        "ring": "focus_ring",
        "success": "ok",
        "warning": "warn",
        "destructive": "fail",
        "info": "info",
        "code": {
          "background": "code_bg",
          "foreground": "code_text",
          "border": "code_border",
          "selection": "code_selection"
        }
      },
      "status_language": {
        "allowed": ["[OK]", "[PASS]", "[FAIL]", "[RISK]", "[BLOCKER]", "[UNKNOWN]"],
        "mapping": {
          "[OK]": "ok",
          "[PASS]": "ok",
          "[FAIL]": "fail",
          "[BLOCKER]": "fail",
          "[RISK]": "warn",
          "[UNKNOWN]": "text_faint"
        }
      }
    },

    "typography": {
      "font_pairing": {
        "ui": "IBM Plex Sans (fallback: Inter, system-ui)",
        "mono": "IBM Plex Mono (fallback: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace)"
      },
      "google_fonts_import": [
        "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap"
      ],
      "scale_tailwind": {
        "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
        "h2": "text-base md:text-lg font-medium text-[color:var(--muted-foreground)]",
        "body": "text-sm md:text-base",
        "small": "text-xs",
        "mono": "font-mono text-xs md:text-sm leading-5"
      },
      "density_rules": {
        "line_height": {
          "ui": "leading-6",
          "mono": "leading-5"
        },
        "numbers": "Все числовые метрики (token, counts, line) — tabular-nums (Tailwind: tabular-nums)."
      }
    },

    "spacing": {
      "base": "4px grid",
      "recommended": {
        "panel_padding": "p-4 (desktop), p-3 (mobile)",
        "row_gap": "gap-2",
        "section_gap": "gap-4",
        "table_cell_padding": "px-3 py-2",
        "editor_gutter": "px-3"
      }
    },

    "radius_shadow": {
      "radius": {
        "sm": "6px",
        "md": "10px",
        "lg": "14px"
      },
      "shadow": {
        "panel": "shadow-[0_1px_0_rgba(0,0,0,0.04),0_8px_24px_rgba(0,0,0,0.06)]",
        "focus": "ring-2 ring-[color:var(--ring)] ring-offset-2 ring-offset-[color:var(--background)]"
      }
    }
  },

  "layout": {
    "grid": {
      "desktop_1920x800": {
        "structure": "2-column split with fixed header",
        "columns": "Left: editor 58% (min 720px). Right: report 42% (min 520px).",
        "header": "Sticky top bar 56px with actions + status summary.",
        "panes": "Both panes independently scrollable (ScrollArea)."
      },
      "desktop_1440": {
        "columns": "Left 55% / Right 45%",
        "behavior": "If width < 1200px: switch to Tabs (Editor/Report/Prompt/Map)."
      },
      "tablet_768": {
        "structure": "Single column with Tabs",
        "tabs": "Редактор | Отчет | Prompt | Map",
        "actions": "Actions collapse into overflow menu (DropdownMenu)"
      }
    },
    "no_centering_rule": "Контент не центрировать. Использовать max-w-none, full-width рабочую область."
  },

  "components": {
    "component_path": {
      "shadcn_primary": [
        "/app/frontend/src/components/ui/button.jsx",
        "/app/frontend/src/components/ui/card.jsx",
        "/app/frontend/src/components/ui/tabs.jsx",
        "/app/frontend/src/components/ui/table.jsx",
        "/app/frontend/src/components/ui/badge.jsx",
        "/app/frontend/src/components/ui/separator.jsx",
        "/app/frontend/src/components/ui/scroll-area.jsx",
        "/app/frontend/src/components/ui/resizable.jsx",
        "/app/frontend/src/components/ui/textarea.jsx",
        "/app/frontend/src/components/ui/input.jsx",
        "/app/frontend/src/components/ui/tooltip.jsx",
        "/app/frontend/src/components/ui/sonner.jsx"
      ]
    },

    "top_bar": {
      "purpose": "Всегда видимые действия + сводка статуса + индикатор несохраненных изменений.",
      "layout": "Left: название файла + dirty flag. Center: status chips. Right: actions.",
      "elements": [
        {
          "type": "text",
          "label": "identity/personas/expert.md",
          "class": "font-mono text-xs md:text-sm text-[color:var(--muted-foreground)]",
          "data-testid": "persona-file-path"
        },
        {
          "type": "badge",
          "label": "НЕ СОХРАНЕНО",
          "visibility": "only when dirty",
          "class": "rounded-md border border-[color:var(--border)] bg-[color:var(--surface_2)] text-[color:var(--text)] text-xs font-medium",
          "data-testid": "unsaved-changes-indicator"
        },
        {
          "type": "status_summary",
          "content": "[PASS]/[FAIL] + N failed checks + token cost",
          "class": "flex items-center gap-2",
          "data-testid": "validation-summary"
        }
      ],
      "actions": [
        {
          "label": "Проверить",
          "variant": "default",
          "data-testid": "validate-button"
        },
        {
          "label": "Сохранить",
          "variant": "secondary",
          "data-testid": "save-button"
        },
        {
          "label": "Сброс к canonical",
          "variant": "outline",
          "data-testid": "reset-canonical-button"
        },
        {
          "label": "Копировать",
          "variant": "outline",
          "data-testid": "copy-to-clipboard-button"
        },
        {
          "label": "Скачать .md",
          "variant": "outline",
          "data-testid": "download-md-button"
        }
      ]
    },

    "editor_pane": {
      "container": "Card with header row + ScrollArea",
      "header": "Left: 'Редактор'. Right: line/char count + last validated timestamp.",
      "editor": {
        "implementation_note": "Если Monaco/CodeMirror не подключены — использовать Textarea + кастомный line-number gutter (виртуализация опционально).",
        "visual": {
          "bg": "var(--code-bg)",
          "text": "var(--code-text)",
          "border": "var(--code-border)",
          "font": "mono",
          "line_numbers": "Отдельная колонка слева, приглушенный цвет, tabular-nums"
        },
        "classes": "bg-[color:var(--code-bg)] text-[color:var(--code-text)] border border-[color:var(--code-border)] rounded-[14px]",
        "data-testid": "persona-editor"
      },
      "micro_interactions": {
        "selection": "Использовать явный цвет выделения (var(--code-selection)).",
        "search": "Ctrl+F открывает Dialog с Input (не браузерный find).",
        "dirty": "При изменении — включать 'НЕ СОХРАНЕНО' и блокировать Reset/Save только при network error."
      }
    },

    "validation_report": {
      "structure": "Сверху: Metrics strip. Ниже: список 48 checks (виртуализировать при необходимости).",
      "metrics_strip": {
        "items": [
          "Всего проверок: 48",
          "FAIL: N",
          "PASS: 48-N",
          "Token(OpenAkita): X",
          "Token(Cyrillic-aware): Y"
        ],
        "component": "Card + inline Table-like grid",
        "class": "grid grid-cols-2 md:grid-cols-5 gap-2",
        "data-testid": "validation-metrics-strip"
      },
      "check_row": {
        "layout": "Left: status token [PASS]/[FAIL]/[RISK]. Middle: rule-id. Right: короткое сообщение + optional line refs.",
        "no_icons": "Не использовать иконки. Только текст + цвет + border.",
        "classes": {
          "row": "flex items-start justify-between gap-3 px-3 py-2 border-b border-[color:var(--border)]",
          "status": "font-mono text-xs tabular-nums",
          "rule_id": "font-mono text-xs text-[color:var(--text_muted)]",
          "message": "text-sm text-[color:var(--text)]"
        },
        "data-testid": "validation-check-row"
      },
      "filters": {
        "recommended": "Tabs: Все | FAIL | RISK | PASS",
        "component": "Tabs",
        "data-testid": "validation-filter-tabs"
      }
    },

    "parsed_values_table": {
      "component": "Table",
      "columns": ["dimension", "expected", "actual", "enum_valid"],
      "format": {
        "dimension": "mono",
        "expected_actual": "mono + tabular-nums",
        "enum_valid": "[OK]/[FAIL] token"
      },
      "data-testid": "parsed-values-table"
    },

    "system_prompt_preview": {
      "component": "Card + ScrollArea",
      "header": "System Prompt Preview (exact) + token costs",
      "body": "pre-like block with mono font; copy button",
      "classes": "bg-[color:var(--surface)]",
      "prompt_block_classes": "bg-[color:var(--code-bg)] text-[color:var(--code-text)] border border-[color:var(--code-border)] rounded-[14px] p-3 font-mono text-xs leading-5 whitespace-pre-wrap",
      "data-testid": "system-prompt-preview"
    },

    "section_map": {
      "component": "Table or dense list",
      "columns": ["section", "parsed", "injected", "ignored"],
      "status": "Use bracket tokens + color",
      "data-testid": "section-map"
    },

    "alerts_toasts": {
      "inline": {
        "component": "Alert",
        "variants": ["default", "destructive"],
        "copy": {
          "network_error": "[BLOCKER] Ошибка сети. /api недоступен.",
          "missing_file": "[BLOCKER] Файл не найден: identity/personas/expert.md",
          "save_error": "[FAIL] Сохранение не выполнено. Код: {status}."
        },
        "data-testid": "inline-alert"
      },
      "toast": {
        "component": "sonner",
        "rules": "Только фактические события: сохранено, скопировано, скачано, проверка завершена.",
        "data-testid": "toast"
      }
    },

    "buttons": {
      "style": "Professional/Corporate: medium radius, tonal fill, minimal shadow",
      "variants": {
        "primary": "Validate",
        "secondary": "Save",
        "outline": "Copy/Download/Reset",
        "destructive": "Reset to canonical (если подтверждение через AlertDialog)"
      },
      "motion": {
        "hover": "background shade shift + border emphasis",
        "press": "scale-[0.98]",
        "focus": "visible ring"
      },
      "data-testid_rule": "Каждая кнопка обязана иметь data-testid"
    }
  },

  "motion": {
    "principles": {
      "duration_ms": {"fast": 120, "normal": 180},
      "easing": "cubic-bezier(0.2, 0.8, 0.2, 1)",
      "no_bounce": true,
      "no_parallax": true
    },
    "allowed": [
      "Tabs content fade-in (opacity only)",
      "Row highlight on update (background-color transition only)",
      "Button hover/press (color + scale)"
    ],
    "forbidden": ["transition: all", "large entrance animations", "spring/bounce"]
  },

  "accessibility": {
    "keyboard": {
      "requirements": [
        "Tab order: Top bar actions -> Editor -> Report filters -> Report list",
        "Ctrl+S triggers Save",
        "Ctrl+Enter triggers Validate",
        "Esc closes dialogs"
      ]
    },
    "contrast": "Все текстовые пары должны быть WCAG AA минимум. Для mono мелкого текста — стремиться к AAA.",
    "focus": "Всегда видимый focus ring (не полагаться на outline: none).",
    "reduced_motion": "Уважать prefers-reduced-motion: отключать fade transitions."
  },

  "testing": {
    "data_testid": {
      "convention": "kebab-case, описывает роль элемента",
      "must_cover": [
        "все кнопки действий",
        "редактор",
        "сводка статуса",
        "метрики",
        "строки проверок",
        "таблица parsed values",
        "prompt preview",
        "section map",
        "inline errors"
      ]
    }
  },

  "image_urls": {
    "policy": "Изображения не использовать (developer tool, запрет на декоративность).",
    "items": []
  },

  "instructions_to_main_agent": [
    "UI тексты строго на русском; English technical terms (prompt, token, parser, regex, enum) не переводить.",
    "Никаких emoji/иконок-эмодзи. Для статусов использовать только текстовые маркеры в квадратных скобках.",
    "Не использовать прозрачные фоны: каждый контейнер/панель имеет явный background.",
    "Сделать split layout через shadcn Resizable на desktop; на <1200px переключаться на Tabs.",
    "Редактор: если нет Monaco/CodeMirror — реализовать Textarea + line-number gutter; обеспечить моноширинный шрифт и tabular-nums.",
    "Отчет: список 48 checks — плотный, без иконок; фильтры через Tabs; строки с rule-id и ссылками на строки файла.",
    "Token cost показывать двумя числами рядом, с подписью оценщика.",
    "Все интерактивные элементы и ключевые метрики обязаны иметь data-testid.",
    "Не применять transition: all. Только точечные transitions (background-color, border-color, opacity).",
    "Удалить/не использовать текущий App.css центрирующий шаблон CRA; не делать .App { text-align:center }.",
    "Подключить Google Fonts IBM Plex Sans + IBM Plex Mono в index.css (или через <link> в public/index.html) и обновить font-family tokens."
  ],

  "general_ui_ux_design_guidelines_appendix": "<General UI UX Design Guidelines>  \n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}
