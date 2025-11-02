# Tech Context: Technical Setup và Tools

## Technologies Used

### Document Format
- **LaTeX**: Academic document preparation system
- **pdfLaTeX**: Compilation engine
- **Vietnamese encoding**: UTF-8 với T5 font encoding
- **Bibliography**: BibTeX format

### LaTeX Packages (từ main.tex)
- `vntex`: Vietnamese text support
- `hyperref`: Hyperlinks và bookmarks
- `graphicx`: Image handling
- `inputenc`: UTF-8 input encoding
- `amsmath, amssymb`: Mathematical symbols
- `geometry`: Page layout
- Custom style: `setting/uetthesis.sty`

## Development Setup

### IDE
- Visual Studio Code
- LaTeX Workshop extension (implied)

### Build System
- `latexmk`: Automated LaTeX compilation
- Multiple passes for references
- SyncTeX for source-PDF synchronization

### File Structure
```
/home/ldkien/Downloads/NLNNLT/
├── main.tex              # Main document
├── cover_page.tex        # Cover page
├── notions.tex          # Definitions/notations
├── references.bib       # Bibliography
├── setting/             # Custom styles
│   ├── uetthesis.sty
│   ├── bkthesis.sty
│   └── cs.sty
└── images/              # Image assets
```

## Technical Constraints

### Encoding Issues
- **Current problem**: Zero-width space (U+200B) trong text
- **Solution**: Cần remove invisible Unicode characters
- **Vietnamese characters**: Phải dùng proper T5 encoding

### Hyperref Warnings
- Composite letters không defined in PD1 encoding
- Ảnh hưởng đến Vietnamese diacritics
- **Solution**: Use `\texorpdfstring` cho bookmarks

### Build Warnings
- Overfull hbox cho URLs dài
- Label changes require multiple compilations
- File references may change

## Dependencies

### Required LaTeX Packages
```latex
\usepackage[utf8]{inputenc}
\usepackage[T5]{fontenc}
\usepackage{vntex}
\usepackage[unicode]{hyperref}
\usepackage{graphicx}
\usepackage{amsmath}
```

### Font Requirements
- Times New Roman (urwvn fonts)
- T5 encoding for Vietnamese

## Build Process

### Standard Workflow
```bash
latexmk -pdf main.tex
```

### Output Files Generated
- `main.pdf`: Final document
- `main.aux`: Auxiliary file (references)
- `main.log`: Build log
- `main.out`: Hyperref outline
- `main.toc`: Table of contents
- `main.lof`: List of figures
- `main.synctex.gz`: SyncTeX data

## Quality Requirements

### Academic Standards
- Proper citations (bibliography)
- Figure captions và references
- Page numbering
- Table of contents
- List of figures

### Language Quality
- Academic Vietnamese
- Technical terminology consistency
- Proper grammar và spelling

## Testing Approach

### Compilation Testing
1. Run `latexmk -pdf main.tex`
2. Check for errors in log
3. Verify PDF output
4. Check hyperref bookmarks

### Content Verification
1. Check chapter structure
2. Verify cross-references
3. Validate bibliography entries
4. Review figure placements

## Known Issues (Current File)

### From Build Log
1. **Line 716**: Unicode U+200B (zero-width space)
2. **Hyperref warnings**: Vietnamese composite letters
3. **Overfull hbox**: Long URLs in references (lines 753-766)
4. **References changed**: Requires rerun

### Resolution Strategy
1. Clean invisible Unicode characters
2. Properly escape Vietnamese in hyperref
3. Break long URLs or use `\url{}` command
4. Run compilation multiple times
