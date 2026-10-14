"""
Central Theme Registry and Palette Resolver for Pixel Readme Kit.
Acts as Single Source of Truth for base themes, presets, and mode resolution.
"""

import os
import json
from typing import Dict, Any, Optional, Tuple, List
from generator.themes.color_utils import darken_hex, is_light_color
from generator.themes.models import ThemeDefinition


# Built-in handcrafted base themes (guarantees pixel-perfect backward compatibility)
BASE_THEME_PALETTES: Dict[str, Dict[str, Dict[str, str]]] = {
    "cyberpunk": {
        "dark": {
            "bg": "rgba(10, 14, 23, 0.85)",
            "panel": "rgba(15, 23, 38, 0.82)",
            "border": "rgba(30, 41, 59, 0.85)",
            "primary": "#00C8D7",
            "accent": "#A855F7",
            "tertiary": "#FF0055",
            "title_front": "#00C8D7",
            "title_mid": "#006B74",
            "title_dark": "#002B2F",
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#00D26A",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F6F8FA",
            "panel": "#EAEFF5",
            "border": "#D0D7DE",
            "primary": "#0969DA",
            "accent": "#8250DF",
            "tertiary": "#CF222E",
            "title_front": "#0969DA",
            "title_mid": "#0550AE",
            "title_dark": "#033D8B",
            "text_main": "#1F2328",
            "text_dim": "#57606A",
            "success": "#1A7F37",
            "warning": "#9A6700",
            "grid_op": "0.10"
        }
    },
    "tactical": {
        "dark": {
            "bg": "rgba(20, 14, 6, 0.88)",
            "panel": "rgba(30, 22, 10, 0.82)",
            "border": "rgba(50, 36, 16, 0.85)",
            "primary": "#F59E0B",
            "accent": "#EA580C",
            "tertiary": "#EF4444",
            "title_front": "#F59E0B",
            "title_mid": "#92400E",
            "title_dark": "#451A03",
            "text_main": "#FFFBEB",
            "text_dim": "#D97706",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#FFFBEB",
            "panel": "#FEF3C7",
            "border": "#FDE68A",
            "primary": "#B45309",
            "accent": "#C2410C",
            "tertiary": "#B91C1C",
            "title_front": "#B45309",
            "title_mid": "#78350F",
            "title_dark": "#451A03",
            "text_main": "#1F2937",
            "text_dim": "#6B7280",
            "success": "#15803D",
            "warning": "#B45309",
            "grid_op": "0.10"
        }
    },
    "minimal": {
        "dark": {
            "bg": "rgba(15, 18, 30, 0.85)",
            "panel": "rgba(22, 27, 46, 0.80)",
            "border": "rgba(41, 46, 66, 0.85)",
            "primary": "#4F8BFF",
            "accent": "#A855F7",
            "tertiary": "#06B6D4",
            "title_front": "#4F8BFF",
            "title_mid": "#2563EB",
            "title_dark": "#1E3A8A",
            "text_main": "#F1F5F9",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#1D4ED8",
            "accent": "#6D28D9",
            "tertiary": "#0891B2",
            "title_front": "#1D4ED8",
            "title_mid": "#1E40AF",
            "title_dark": "#0F172A",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.10"
        }
    },
    "amber": {
        "dark": {
            "bg": "rgba(20, 12, 5, 0.90)",
            "panel": "rgba(32, 18, 8, 0.85)",
            "border": "rgba(55, 32, 15, 0.85)",
            "primary": "#FFB000",
            "accent": "#FFE57F",
            "tertiary": "#FF8800",
            "title_front": "#FFB000",
            "title_mid": "#D97706",
            "title_dark": "#78350F",
            "text_main": "#FFFBEB",
            "text_dim": "#F59E0B",
            "success": "#79FFE1",
            "warning": "#FF5500",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#FFFBEB",
            "panel": "#FEF3C7",
            "border": "#FDE68A",
            "primary": "#D97706",
            "accent": "#B45309",
            "tertiary": "#92400E",
            "title_front": "#B45309",
            "title_mid": "#78350F",
            "title_dark": "#451A03",
            "text_main": "#451A03",
            "text_dim": "#92400E",
            "success": "#059669",
            "warning": "#DC2626",
            "grid_op": "0.10"
        }
    },
    "tokyo": {
        "dark": {
            "bg": "rgba(15, 18, 28, 0.92)",
            "panel": "rgba(23, 27, 44, 0.85)",
            "border": "rgba(42, 49, 78, 0.85)",
            "primary": "#7AA2F7",
            "accent": "#7DCFFF",
            "tertiary": "#BB9AF7",
            "title_front": "#7AA2F7",
            "title_mid": "#565F89",
            "title_dark": "#24283B",
            "text_main": "#C0CAF5",
            "text_dim": "#7982A9",
            "success": "#9ECE6A",
            "warning": "#E0AF68",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#2E56B6",
            "accent": "#0284C7",
            "tertiary": "#6D28D9",
            "title_front": "#1E3A8A",
            "title_mid": "#2563EB",
            "title_dark": "#0F172A",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "matrix": {
        "dark": {
            "bg": "rgba(5, 20, 10, 0.92)",
            "panel": "rgba(10, 32, 16, 0.85)",
            "border": "rgba(20, 60, 30, 0.85)",
            "primary": "#00FF66",
            "accent": "#79FFE1",
            "tertiary": "#00DD44",
            "title_front": "#00FF66",
            "title_mid": "#00AA44",
            "title_dark": "#005522",
            "text_main": "#E8FDF0",
            "text_dim": "#55FF99",
            "success": "#00FF66",
            "warning": "#FFE600",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F0FDF4",
            "panel": "#DCFCE7",
            "border": "#BBF7D0",
            "primary": "#15803D",
            "accent": "#0D9488",
            "tertiary": "#166534",
            "title_front": "#166534",
            "title_mid": "#15803D",
            "title_dark": "#14532D",
            "text_main": "#14532D",
            "text_dim": "#166534",
            "success": "#15803D",
            "warning": "#CA8A04",
            "grid_op": "0.08"
        }
    },
    "clean-mono": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.85)",
            "panel": "rgba(30, 41, 59, 0.80)",
            "border": "rgba(51, 65, 85, 0.85)",
            "primary": "#E2E8F0",
            "accent": "#94A3B8",
            "tertiary": "#CBD5E1",
            "title_front": "#F8FAFC",
            "title_mid": "#CBD5E1",
            "title_dark": "#64748B",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FFFFFF",
            "panel": "#F1F5F9",
            "border": "#CBD5E1",
            "primary": "#0F172A",
            "accent": "#475569",
            "tertiary": "#64748B",
            "title_front": "#0F172A",
            "title_mid": "#334155",
            "title_dark": "#64748B",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "corporate-blue": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.88)",
            "panel": "rgba(30, 41, 59, 0.82)",
            "border": "rgba(30, 58, 138, 0.85)",
            "primary": "#38BDF8",
            "accent": "#818CF8",
            "tertiary": "#0284C7",
            "title_front": "#38BDF8",
            "title_mid": "#0284C7",
            "title_dark": "#0369A1",
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#22C55E",
            "warning": "#EAB308",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F0F9FF",
            "panel": "#E0F2FE",
            "border": "#BAE6FD",
            "primary": "#0284C7",
            "accent": "#4F46E5",
            "tertiary": "#0369A1",
            "title_front": "#0369A1",
            "title_mid": "#075985",
            "title_dark": "#0C4A6E",
            "text_main": "#0C4A6E",
            "text_dim": "#0369A1",
            "success": "#16A34A",
            "warning": "#CA8A04",
            "grid_op": "0.08"
        }
    },
    "academic-paper": {
        "dark": {
            "bg": "rgba(24, 24, 27, 0.88)",
            "panel": "rgba(39, 39, 42, 0.82)",
            "border": "rgba(63, 63, 70, 0.85)",
            "primary": "#60A5FA",
            "accent": "#F59E0B",
            "tertiary": "#38BDF8",
            "title_front": "#93C5FD",
            "title_mid": "#3B82F6",
            "title_dark": "#1D4ED8",
            "text_main": "#F4F4F5",
            "text_dim": "#A1A1AA",
            "success": "#10B981",
            "warning": "#D97706",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FAFAF9",
            "panel": "#F5F5F4",
            "border": "#E7E5E4",
            "primary": "#1C1917",
            "accent": "#B45309",
            "tertiary": "#2563EB",
            "title_front": "#1C1917",
            "title_mid": "#44403C",
            "title_dark": "#78716C",
            "text_main": "#1C1917",
            "text_dim": "#78716C",
            "success": "#15803D",
            "warning": "#B45309",
            "grid_op": "0.06"
        }
    },
    "modern-slate": {
        "dark": {
            "bg": "rgba(15, 23, 30, 0.88)",
            "panel": "rgba(22, 33, 46, 0.82)",
            "border": "rgba(30, 41, 59, 0.85)",
            "primary": "#2DD4BF",
            "accent": "#A78BFA",
            "tertiary": "#F43F5E",
            "title_front": "#2DD4BF",
            "title_mid": "#0D9488",
            "title_dark": "#115E59",
            "text_main": "#F1F5F9",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#0F766E",
            "accent": "#6D28D9",
            "tertiary": "#BE123C",
            "title_front": "#0F766E",
            "title_mid": "#115E59",
            "title_dark": "#134E4A",
            "text_main": "#0F172A",
            "text_dim": "#475569",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "slate-dark": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.90)",
            "panel": "rgba(30, 41, 59, 0.85)",
            "border": "rgba(51, 65, 85, 0.85)",
            "primary": "#38BDF8",
            "accent": "#818CF8",
            "tertiary": "#06B6D4",
            "title_front": "#38BDF8",
            "title_mid": "#0284C7",
            "title_dark": "#0369A1",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#0284C7",
            "accent": "#4F46E5",
            "tertiary": "#0891B2",
            "title_front": "#0284C7",
            "title_mid": "#0369A1",
            "title_dark": "#0C4A6E",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "nordic-frost": {
        "dark": {
            "bg": "rgba(10, 20, 32, 0.92)",
            "panel": "rgba(16, 30, 48, 0.85)",
            "border": "rgba(38, 64, 98, 0.85)",
            "primary": "#E0F2FE",
            "accent": "#38BDF8",
            "tertiary": "#7DD3FC",
            "title_front": "#F0F9FF",
            "title_mid": "#BAE6FD",
            "title_dark": "#38BDF8",
            "text_main": "#F0F9FF",
            "text_dim": "#94A3B8",
            "success": "#34D399",
            "warning": "#FBBF24",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#F0F9FF",
            "panel": "#E0F2FE",
            "border": "#BAE6FD",
            "primary": "#0369A1",
            "accent": "#0284C7",
            "tertiary": "#075985",
            "title_front": "#0C4A6E",
            "title_mid": "#075985",
            "title_dark": "#0369A1",
            "text_main": "#0C4A6E",
            "text_dim": "#0369A1",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "linear-violet": {
        "dark": {
            "bg": "rgba(8, 9, 13, 0.94)",
            "panel": "rgba(18, 19, 29, 0.88)",
            "border": "rgba(45, 43, 67, 0.85)",
            "primary": "#8B5CF6",
            "accent": "#C084FC",
            "tertiary": "#A855F7",
            "title_front": "#A78BFA",
            "title_mid": "#7C3AED",
            "title_dark": "#4C1D95",
            "text_main": "#F5F3FF",
            "text_dim": "#A78BFA",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#FAF5FF",
            "panel": "#F3E8FF",
            "border": "#E9D5FF",
            "primary": "#6D28D9",
            "accent": "#7C3AED",
            "tertiary": "#8B5CF6",
            "title_front": "#5B21B6",
            "title_mid": "#6D28D9",
            "title_dark": "#7C3AED",
            "text_main": "#2E1065",
            "text_dim": "#6B21A8",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "emerald-clean": {
        "dark": {
            "bg": "rgba(6, 20, 16, 0.92)",
            "panel": "rgba(12, 34, 27, 0.86)",
            "border": "rgba(20, 60, 48, 0.85)",
            "primary": "#10B981",
            "accent": "#34D399",
            "tertiary": "#059669",
            "title_front": "#34D399",
            "title_mid": "#059669",
            "title_dark": "#047857",
            "text_main": "#ECFDF5",
            "text_dim": "#6EE7B7",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F0FDF4",
            "panel": "#DCFCE7",
            "border": "#BBF7D0",
            "primary": "#15803D",
            "accent": "#16A34A",
            "tertiary": "#166534",
            "title_front": "#14532D",
            "title_mid": "#15803D",
            "title_dark": "#166534",
            "text_main": "#14532D",
            "text_dim": "#166534",
            "success": "#15803D",
            "warning": "#CA8A04",
            "grid_op": "0.08"
        }
    },
    "enterprise-navy": {
        "dark": {
            "bg": "rgba(10, 25, 47, 0.94)",
            "panel": "rgba(17, 34, 64, 0.88)",
            "border": "rgba(35, 53, 84, 0.85)",
            "primary": "#64FFDA",
            "accent": "#CCD6F6",
            "tertiary": "#8892B0",
            "title_front": "#64FFDA",
            "title_mid": "#20C997",
            "title_dark": "#0D6E54",
            "text_main": "#CCD6F6",
            "text_dim": "#8892B0",
            "success": "#64FFDA",
            "warning": "#FFB86C",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F4F7FB",
            "panel": "#E8EEF5",
            "border": "#D1DCED",
            "primary": "#0A192F",
            "accent": "#1E3A8A",
            "tertiary": "#3B82F6",
            "title_front": "#0A192F",
            "title_mid": "#1E3A8A",
            "title_dark": "#172554",
            "text_main": "#0A192F",
            "text_dim": "#475569",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "swiss-mono": {
        "dark": {
            "bg": "rgba(10, 10, 10, 0.95)",
            "panel": "rgba(20, 20, 20, 0.90)",
            "border": "rgba(50, 50, 50, 0.85)",
            "primary": "#FFFFFF",
            "accent": "#E5E5E5",
            "tertiary": "#A3A3A3",
            "title_front": "#FFFFFF",
            "title_mid": "#D4D4D4",
            "title_dark": "#737373",
            "text_main": "#FFFFFF",
            "text_dim": "#A3A3A3",
            "success": "#22C55E",
            "warning": "#EAB308",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FFFFFF",
            "panel": "#F5F5F5",
            "border": "#E5E5E5",
            "primary": "#000000",
            "accent": "#262626",
            "tertiary": "#525252",
            "title_front": "#000000",
            "title_mid": "#262626",
            "title_dark": "#404040",
            "text_main": "#000000",
            "text_dim": "#525252",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "executive-slate": {
        "dark": {
            "bg": "rgba(15, 20, 25, 0.92)",
            "panel": "rgba(25, 33, 41, 0.86)",
            "border": "rgba(45, 55, 72, 0.85)",
            "primary": "#94A3B8",
            "accent": "#CBD5E1",
            "tertiary": "#64748B",
            "title_front": "#F1F5F9",
            "title_mid": "#94A3B8",
            "title_dark": "#475569",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#334155",
            "accent": "#475569",
            "tertiary": "#64748B",
            "title_front": "#0F172A",
            "title_mid": "#1E293B",
            "title_dark": "#334155",
            "text_main": "#0F172A",
            "text_dim": "#475569",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "excali-dark": {
        "dark": {
            "bg": "rgba(18, 18, 18, 0.95)",
            "panel": "rgba(28, 28, 28, 0.90)",
            "border": "#E0E0E0",
            "primary": "#A78BFA",
            "accent": "#6EE7B7",
            "tertiary": "#FDE047",
            "title_front": "#F3F4F6",
            "title_mid": "#E0E0E0",
            "title_dark": "#A78BFA",
            "text_main": "#F3F4F6",
            "text_dim": "#9CA3AF",
            "success": "#6EE7B7",
            "warning": "#FDE047",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FDFDFD",
            "panel": "#F4F4F5",
            "border": "#1F2937",
            "primary": "#4F46E5",
            "accent": "#059669",
            "tertiary": "#D97706",
            "title_front": "#111827",
            "title_mid": "#374151",
            "title_dark": "#4F46E5",
            "text_main": "#111827",
            "text_dim": "#4B5563",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.06"
        }
    },
    "whiteboard": {
        "dark": {
            "bg": "rgba(24, 24, 27, 0.94)",
            "panel": "rgba(39, 39, 42, 0.90)",
            "border": "#FAFAFA",
            "primary": "#38BDF8",
            "accent": "#F87171",
            "tertiary": "#FBBF24",
            "title_front": "#FAFAFA",
            "title_mid": "#E4E4E7",
            "title_dark": "#38BDF8",
            "text_main": "#FAFAFA",
            "text_dim": "#A1A1AA",
            "success": "#34D399",
            "warning": "#FBBF24",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FFFFFF",
            "panel": "#F8FAFC",
            "border": "#18181B",
            "primary": "#2563EB",
            "accent": "#DC2626",
            "tertiary": "#D97706",
            "title_front": "#0F172A",
            "title_mid": "#1E293B",
            "title_dark": "#2563EB",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#DC2626",
            "grid_op": "0.06"
        }
    },
    "notebook-graph": {
        "dark": {
            "bg": "rgba(23, 25, 30, 0.94)",
            "panel": "rgba(33, 37, 44, 0.90)",
            "border": "#CBD5E1",
            "primary": "#F3F4F6",
            "accent": "#FACC15",
            "tertiary": "#FB923C",
            "title_front": "#F3F4F6",
            "title_mid": "#E2E8F0",
            "title_dark": "#FACC15",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#4ADE80",
            "warning": "#FACC15",
            "grid_op": "0.08"
        },
        "light": {
            "bg": "#FAF7F2",
            "panel": "#F3EFEA",
            "border": "#78716C",
            "primary": "#1E3A8A",
            "accent": "#D97706",
            "tertiary": "#DC2626",
            "title_front": "#1C1917",
            "title_mid": "#44403C",
            "title_dark": "#1E3A8A",
            "text_main": "#1C1917",
            "text_dim": "#78716C",
            "success": "#15803D",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "blueprint-sketch": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.94)",
            "panel": "rgba(24, 35, 60, 0.90)",
            "border": "#38BDF8",
            "primary": "#F8FAFC",
            "accent": "#38BDF8",
            "tertiary": "#7DD3FC",
            "title_front": "#F8FAFC",
            "title_mid": "#BAE6FD",
            "title_dark": "#0284C7",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#34D399",
            "warning": "#FBBF24",
            "grid_op": "0.10"
        },
        "light": {
            "bg": "#F0F9FF",
            "panel": "#E0F2FE",
            "border": "#0369A1",
            "primary": "#0369A1",
            "accent": "#0284C7",
            "tertiary": "#075985",
            "title_front": "#0C4A6E",
            "title_mid": "#075985",
            "title_dark": "#0369A1",
            "text_main": "#0C4A6E",
            "text_dim": "#0369A1",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.10"
        }
    },
    "modern-clean": {
        "dark": {
            "bg": "rgba(15, 23, 42, 0.90)",
            "panel": "rgba(30, 41, 59, 0.85)",
            "border": "rgba(51, 65, 85, 0.85)",
            "primary": "#38BDF8",
            "accent": "#818CF8",
            "tertiary": "#06B6D4",
            "title_front": "#38BDF8",
            "title_mid": "#0284C7",
            "title_dark": "#0369A1",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#10B981",
            "warning": "#F59E0B",
            "grid_op": "0.07"
        },
        "light": {
            "bg": "#F8FAFC",
            "panel": "#F1F5F9",
            "border": "#E2E8F0",
            "primary": "#0284C7",
            "accent": "#4F46E5",
            "tertiary": "#0891B2",
            "title_front": "#0284C7",
            "title_mid": "#0369A1",
            "title_dark": "#0C4A6E",
            "text_main": "#0F172A",
            "text_dim": "#64748B",
            "success": "#16A34A",
            "warning": "#D97706",
            "grid_op": "0.08"
        }
    },
    "rough-doodle": {
        "dark": {
            "bg": "rgba(28, 30, 36, 0.95)",
            "panel": "rgba(38, 41, 50, 0.90)",
            "border": "#94A3B8",
            "primary": "#818CF8",
            "accent": "#34D399",
            "tertiary": "#FBBF24",
            "title_front": "#F8FAFC",
            "title_mid": "#94A3B8",
            "title_dark": "#818CF8",
            "text_main": "#F8FAFC",
            "text_dim": "#94A3B8",
            "success": "#34D399",
            "warning": "#FBBF24",
            "grid_op": "0.06"
        },
        "light": {
            "bg": "#FDFDFD",
            "panel": "#F4F4F5",
            "border": "#1F2937",
            "primary": "#4F46E5",
            "accent": "#059669",
            "tertiary": "#D97706",
            "title_front": "#111827",
            "title_mid": "#374151",
            "title_dark": "#4F46E5",
            "text_main": "#111827",
            "text_dim": "#4B5563",
            "success": "#059669",
            "warning": "#D97706",
            "grid_op": "0.06"
        }
    }
}

# Standard style and name aliases
THEME_ALIASES: Dict[str, str] = {
    "academic": "academic-paper",
    "paper": "academic-paper",
    "academic_paper": "academic-paper",
    "clean_mono": "clean-mono",
    "corporate": "corporate-blue",
    "corporate_blue": "corporate-blue",
    "modern_slate": "modern-slate",
    "amber_crt": "amber",
    "amber-crt": "amber",
    "matrix_terminal": "matrix",
    "matrix-terminal": "matrix",
    "tokyo_night": "tokyo",
    "tokyo-night": "tokyo",
    "tactical_amber": "tactical",
    "tactical-amber": "tactical",
    "slate_dark": "slate-dark",
    "nordic": "nordic-frost",
    "frost": "nordic-frost",
    "nordic_frost": "nordic-frost",
    "linear_violet": "linear-violet",
    "emerald_clean": "emerald-clean",
    "enterprise_navy": "enterprise-navy",
    "swiss_mono": "swiss-mono",
    "executive_slate": "executive-slate",
    "excali": "excali-dark",
    "excalidraw": "excali-dark",
    "excali_dark": "excali-dark",
    "notebook": "notebook-graph",
    "notebook_graph": "notebook-graph",
    "blueprint": "blueprint-sketch",
    "blueprint_sketch": "blueprint-sketch",
    "modern": "modern-clean",
    "sketch": "rough-doodle",
    "doodle": "rough-doodle",
}

# 3-level architectural classification:
# 1. Styles (3 visual paradigms)
VALID_STYLES: List[str] = ["pixel", "modern", "sketch", "corporate"]

# 2. Canonical Themes (5 geometric flavors across styles)
# In style pixel: 3 themes (cyberpunk, tactical, minimal)
# In style modern: 1 theme (modern-clean)
# In style sketch: 1 theme (rough-doodle)
STYLE_CANONICAL_THEMES: Dict[str, List[str]] = {
    "pixel": [
        "cyberpunk",
        "tactical",
        "minimal",
    ],
    "modern": [
        "modern-clean",
    ],
    "sketch": [
        "rough-doodle",
    ],
    "corporate": [
        "academic-paper",
    ],
}
STYLE_THEMES: Dict[str, List[str]] = STYLE_CANONICAL_THEMES


# All themes and presets accessible per style
STYLE_ALL_THEMES: Dict[str, List[str]] = {
    "pixel": [
        "cyberpunk",
        "tactical",
        "minimal",
        "amber",
        "tokyo",
        "matrix",
        "clean-mono",
    ],
    "modern": [
        "modern-clean",
        "slate-dark",
        "nordic-frost",
        "linear-violet",
        "emerald-clean",
        "modern-slate",
    ],
    "sketch": [
        "rough-doodle",
        "excali-dark",
        "whiteboard",
        "notebook-graph",
        "blueprint-sketch",
    ],
    "corporate": [
        "corporate-blue",
        "academic-paper",
        "enterprise-navy",
        "swiss-mono",
        "executive-slate",
    ],
}

# The 5 canonical themes across all styles
CANONICAL_THEMES: List[str] = [
    "cyberpunk",
    "tactical",
    "minimal",
    "modern-clean",
    "rough-doodle",
]

# 3. Presets / Color Palettes per Theme (Расцветки)
THEME_PRESETS: Dict[str, List[str]] = {
    "cyberpunk": [
        "cyberpunk",
        "neon-matrix",
        "matrix",
        "synthwave",
        "amber",
    ],
    "tactical": [
        "tactical",
        "amber",
    ],
    "minimal": [
        "minimal",
        "tokyo",
        "clean-mono",
    ],
    "modern-clean": [
        "slate-dark",
        "nordic-frost",
        "linear-violet",
        "emerald-clean",
        "modern-slate",
        "clean-mono",
    ],
    "rough-doodle": [
        "excali-dark",
        "whiteboard",
        "notebook-graph",
        "blueprint-sketch",
    ],
}


def load_preset(preset_name_or_path: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Loads custom color palette from a JSON file or named preset in presets/.
    Preserves exact backward compatibility with engine.load_preset.
    """
    if not preset_name_or_path:
        return None
    path = str(preset_name_or_path).strip()
    if os.path.isfile(path):
        target_path = path
    else:
        # Search relative to package presets, repo root, and local cwd
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cands = [
            os.path.join(base_dir, "..", "presets", f"{path}.json"),
            os.path.join(base_dir, "..", "presets", path),
            os.path.join(base_dir, "..", "..", "presets", f"{path}.json"),
            os.path.join(base_dir, "..", "..", "presets", path),
            os.path.join("presets", f"{path}.json"),
            os.path.join("presets", path),
            f"{path}.json"
        ]
        target_path = None
        for c in cands:
            if os.path.isfile(c):
                target_path = c
                break
        if not target_path:
            canonical = THEME_ALIASES.get(path.lower().strip(), path.lower().strip())
            if canonical in BASE_THEME_PALETTES:
                p = BASE_THEME_PALETTES[canonical]["dark"]
                return {
                    "theme": canonical,
                    "primary": p.get("primary"),
                    "secondary": p.get("accent"),
                    "accent": p.get("tertiary"),
                    "success": p.get("success"),
                    "warning": p.get("warning"),
                    "bg_glass": p.get("bg"),
                    "bg_panel": p.get("panel"),
                    "border_subtle": p.get("border")
                }
            return None
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


class ThemeRegistry:
    """Singleton Theme Registry managing all available themes, palettes, and presets."""

    def __init__(self, presets_dir: Optional[str] = None):
        if presets_dir:
            self.presets_dir = presets_dir
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            cand_pkg = os.path.abspath(os.path.join(base_dir, "..", "presets"))
            cand_root = os.path.abspath(os.path.join(base_dir, "..", "..", "presets"))
            if os.path.isdir(cand_pkg):
                self.presets_dir = cand_pkg
            elif os.path.isdir(cand_root):
                self.presets_dir = cand_root
            else:
                self.presets_dir = cand_pkg

        self._palettes: Dict[str, Dict[str, Dict[str, str]]] = {
            k: {m: dict(v[m]) for m in v} for k, v in BASE_THEME_PALETTES.items()
        }
        for alias, target in THEME_ALIASES.items():
            if target in self._palettes:
                self._palettes[alias] = self._palettes[target]

    @property
    def theme_palettes(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Provides direct dictionary access for backward compatibility."""
        return self._palettes

    def list_presets(self) -> List[str]:
        """Returns sorted list of available JSON preset names (scanning both workspace and package presets)."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cand_pkg = os.path.abspath(os.path.join(base_dir, "..", "presets"))
        dirs_to_scan = [self.presets_dir]
        if cand_pkg != self.presets_dir and os.path.isdir(cand_pkg):
            dirs_to_scan.append(cand_pkg)

        names = set()
        for pdir in dirs_to_scan:
            if os.path.isdir(pdir):
                for f in os.listdir(pdir):
                    if f.endswith(".json"):
                        names.add(f[:-5])

        if not names:
            return sorted(list(BASE_THEME_PALETTES.keys()))
        return sorted(list(names))

    def get_themes_for_style(self, style: str) -> List[str]:
        """Returns list of themes and presets available for a specific visual paradigm style."""
        st = (style or "pixel").lower().strip()
        themes = list(STYLE_ALL_THEMES.get(st, []))
        return themes if themes else ["cyberpunk"]

    def get_canonical_themes_for_style(self, style: str) -> List[str]:
        """Returns list of the canonical geometric themes for a style."""
        st = (style or "pixel").lower().strip()
        themes = list(STYLE_CANONICAL_THEMES.get(st, []))
        return themes if themes else ["cyberpunk"]

    def get_presets_for_theme(self, theme: str) -> List[str]:
        """Returns list of color preset slugs (расцветки) for a specific theme."""
        t = (theme or "cyberpunk").lower().strip()
        t = THEME_ALIASES.get(t, t)
        if t in THEME_PRESETS:
            return list(THEME_PRESETS[t])
        for can_theme, presets in THEME_PRESETS.items():
            if t in presets:
                return list(presets)
        return ["cyberpunk"]

    def normalize_style_and_theme(
        self,
        style: Optional[str] = None,
        theme: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Normalizes style (pixel|modern|sketch) and theme/preset.
        Guarantees 100% backward compatibility:
        - If style and theme are provided, preserves both with alias resolution.
        - If theme is provided without style, infers style from theme or preset.
        - If style is provided without theme, returns canonical theme for style.
        - If legacy theme name was passed in style parameter, maps to proper style and theme.
        """
        if theme:
            t_raw = str(theme).lower().strip()
            t = THEME_ALIASES.get(t_raw, t_raw)

            if style and str(style).lower().strip() in VALID_STYLES:
                target_style = str(style).lower().strip()
            else:
                target_style = "pixel"
                for st, themes_list in STYLE_ALL_THEMES.items():
                    if t in themes_list or t_raw in themes_list:
                        target_style = st
                        break
            return target_style, t

        if not style:
            return "pixel", "cyberpunk"

        s_clean = str(style).lower().strip()
        if s_clean in VALID_STYLES:
            def_theme = STYLE_CANONICAL_THEMES.get(s_clean, ["cyberpunk"])[0]
            return s_clean, def_theme

        # Legacy case: style was a theme/preset name passed in style parameter
        s_alias = THEME_ALIASES.get(s_clean, s_clean)
        target_style = "pixel"
        for st, themes_list in STYLE_ALL_THEMES.items():
            if s_alias in themes_list or s_clean in themes_list:
                target_style = st
                break

        return target_style, s_alias

    def resolve_theme(
        self,
        style: Optional[str] = None,
        mode: str = "auto",
        primary: Optional[str] = None,
        accent: Optional[str] = None,
        preset: Optional[str] = None,
        tertiary: Optional[str] = None,
        theme: Optional[str] = None,
    ) -> Tuple[Dict[str, str], str]:
        """
        Resolves final theme color dictionary and CSS variables for SVG rendering.
        Supports both new orthogonal `style` & `theme` parameters and legacy `style="<theme>"` calls.
        Fully backward compatible with engine.resolve_theme.
        """
        target_style, target_theme = self.normalize_style_and_theme(style=style, theme=theme)
        canonical = THEME_ALIASES.get(target_theme, target_theme)
        pal = self._palettes.get(canonical, self._palettes["cyberpunk"])
        dark_vals = dict(pal["dark"])
        light_vals = dict(pal["light"])

        if preset:
            preset_data = load_preset(preset)
            if preset_data:
                p_prim = preset_data.get("primary")
                p_acc = preset_data.get("accent") or preset_data.get("secondary")
                p_tert = preset_data.get("tertiary") or (
                    preset_data.get("accent") if preset_data.get("secondary") else None
                )
                p_succ = preset_data.get("success")
                p_warn = preset_data.get("warning")
                p_bg = preset_data.get("bg_glass") or preset_data.get("bg")
                p_panel = preset_data.get("bg_panel") or preset_data.get("panel")
                p_border = (
                    preset_data.get("border_subtle")
                    or preset_data.get("border_slate")
                    or preset_data.get("border")
                )

                if p_prim and not primary:
                    primary = p_prim
                if p_acc and not accent:
                    accent = p_acc
                if p_tert and not tertiary:
                    tertiary = p_tert
                if p_succ:
                    dark_vals["success"] = p_succ
                    light_vals["success"] = darken_hex(p_succ, 0.7) if is_light_color(p_succ) else p_succ
                if p_warn:
                    dark_vals["warning"] = p_warn
                    light_vals["warning"] = darken_hex(p_warn, 0.7) if is_light_color(p_warn) else p_warn
                if p_bg:
                    dark_vals["bg"] = p_bg
                if p_panel:
                    dark_vals["panel"] = p_panel
                if p_border:
                    dark_vals["border"] = p_border

        if primary:
            dark_vals["primary"] = primary
            dark_vals["title_front"] = primary
            dark_vals["title_mid"] = darken_hex(primary, 0.45)
            dark_vals["title_dark"] = darken_hex(primary, 0.15)
            light_vals["primary"] = darken_hex(primary, 0.7) if is_light_color(primary) else primary
            light_vals["title_front"] = light_vals["primary"]
            light_vals["title_mid"] = darken_hex(light_vals["primary"], 0.6)
            light_vals["title_dark"] = darken_hex(light_vals["primary"], 0.3)

        if accent:
            dark_vals["accent"] = accent
            light_vals["accent"] = darken_hex(accent, 0.7) if is_light_color(accent) else accent

        if tertiary:
            dark_vals["tertiary"] = tertiary
            light_vals["tertiary"] = darken_hex(tertiary, 0.7) if is_light_color(tertiary) else tertiary

        m = mode.lower() if mode else "auto"
        if m == "dark":
            return dark_vals, ""
        elif m == "light":
            return light_vals, ""
        elif m == "transparent":
            res = dict(dark_vals)
            res["bg"] = "none"
            res["panel"] = "none"
            return res, ""
        else:  # "auto" (default: CSS variables + @media)
            colors = {
                "bg": "var(--bg-glass)",
                "panel": "var(--bg-panel)",
                "border": "var(--border-chassis)",
                "primary": "var(--primary)",
                "accent": "var(--accent)",
                "tertiary": "var(--tertiary)",
                "title_front": "var(--title-front)",
                "title_mid": "var(--title-mid)",
                "title_dark": "var(--title-dark)",
                "text_main": "var(--text-main)",
                "text_dim": "var(--text-dim)",
                "success": "var(--status)",
                "warning": "var(--warning)",
                "grid_op": "var(--grid-op)"
            }
            is_light_first = canonical in ("rough-doodle", "academic-paper", "whiteboard")
            root_vals = light_vals if is_light_first else dark_vals
            css_vars = f"""
      :root {{
        --bg-glass: {root_vals['bg']};
        --bg-panel: {root_vals['panel']};
        --border-chassis: {root_vals['border']};
        --primary: {root_vals['primary']};
        --accent: {root_vals['accent']};
        --tertiary: {root_vals['tertiary']};
        --title-front: {root_vals['title_front']};
        --title-mid: {root_vals['title_mid']};
        --title-dark: {root_vals['title_dark']};
        --text-main: {root_vals['text_main']};
        --text-dim: {root_vals['text_dim']};
        --status: {root_vals['success']};
        --warning: {root_vals['warning']};
        --grid-op: {root_vals['grid_op']};
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          --bg-glass: {dark_vals['bg']};
          --bg-panel: {dark_vals['panel']};
          --border-chassis: {dark_vals['border']};
          --primary: {dark_vals['primary']};
          --accent: {dark_vals['accent']};
          --tertiary: {dark_vals['tertiary']};
          --title-front: {dark_vals['title_front']};
          --title-mid: {dark_vals['title_mid']};
          --title-dark: {dark_vals['title_dark']};
          --text-main: {dark_vals['text_main']};
          --text-dim: {dark_vals['text_dim']};
          --status: {dark_vals['success']};
          --warning: {dark_vals['warning']};
          --grid-op: {dark_vals['grid_op']};
        }}
      }}
      @media (prefers-color-scheme: light) {{
        :root {{
          --bg-glass: {light_vals['bg']};
          --bg-panel: {light_vals['panel']};
          --border-chassis: {light_vals['border']};
          --primary: {light_vals['primary']};
          --accent: {light_vals['accent']};
          --tertiary: {light_vals['tertiary']};
          --title-front: {light_vals['title_front']};
          --title-mid: {light_vals['title_mid']};
          --title-dark: {light_vals['title_dark']};
          --text-main: {light_vals['text_main']};
          --text-dim: {light_vals['text_dim']};
          --status: {light_vals['success']};
          --warning: {light_vals['warning']};
          --grid-op: {light_vals['grid_op']};
        }}
      }}
      @media (hover: hover) {{
        .btn-hover:hover, a:hover polygon, a:hover rect {{
          filter: drop-shadow(0 0 6px var(--primary, {root_vals['primary']}));
          cursor: pointer;
          transition: filter 0.2s ease;
        }}
      }}
"""
            return colors, css_vars

    def resolve_colors(self, style=None, primary=None, accent=None, mode="auto", preset=None, tertiary=None, theme=None):
        c, _ = self.resolve_theme(style=style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary, theme=theme)
        return c["primary"], c["accent"], c.get("tertiary", c["accent"])


# Default singleton instance
theme_registry = ThemeRegistry()
THEME_PALETTES = theme_registry.theme_palettes
STYLE_PALETTES = {k: v["dark"] for k, v in THEME_PALETTES.items()}
resolve_theme = theme_registry.resolve_theme
normalize_style_and_theme = theme_registry.normalize_style_and_theme
get_themes_for_style = theme_registry.get_themes_for_style
get_canonical_themes_for_style = theme_registry.get_canonical_themes_for_style
get_presets_for_theme = theme_registry.get_presets_for_theme

def resolve_colors(style=None, primary=None, accent=None, mode="auto", preset=None, tertiary=None, theme=None):
    c, _ = resolve_theme(style=style, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary, theme=theme)
    return c["primary"], c["accent"], c["bg"]
