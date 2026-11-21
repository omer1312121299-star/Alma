# Alma — AI video studio

מערכת להפקת רילס נדל"ן אנכיים (9:16) בעברית, בסגנון `reference/gazi-boulevard-original.mov`.

- `docs/01-reverse-engineering.md` — פירוק מלא של סרטון הרפרנס (תסריט, שוטים, עיצוב, אודיו)
- `docs/02-production-workflow.md` — תוכנית העבודה מבריף ועד MP4, ואיך לבקש שינויים
- `engine/` — מנוע עריכה (Remotion): כל סרטון = `engine/public/projects/<name>/video.json`
- `tools/` — תמלול עברי, מפות לוויין, הנפשת תמונות ב-AI, אפקטים, בקרת איכות
- `CLAUDE.md` — הוראות עבודה ל-Claude

```bash
cd engine && npm install
node scripts/render.mjs gazi-demo      # → engine/out/gazi-demo.mp4
npm run studio                         # עורך ויזואלי בדפדפן (מקומי)
```
