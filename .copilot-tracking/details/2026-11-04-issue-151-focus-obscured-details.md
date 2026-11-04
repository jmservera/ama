---
title: Issue 151 focus not obscured details
ms.date: 2026-11-04
---

Launcher is 3.5rem min height plus 1rem inset, so 6rem padding gives margin. Tests assert padding >= 4.5rem and that every position:fixed rule sits in chat-widget.css (count 2). No-drag test scans web/*.js for draggable, dragstart, mousedown, touchstart.
