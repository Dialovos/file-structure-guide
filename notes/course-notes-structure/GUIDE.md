## TL;DR

Give **every course its own folder**, with the same internal shape in every term: a `README.md` of course facts, and one subfolder per kind of material, **notes**, **readings**, **homework**, **quizzes**, **exams**, and (if the course has one) **project**. Inside, name files by date or assignment number so everything sorts in the order the semester happened. Course facts (instructor, meeting times, grading weights, office hours, deadlines, links) go in the README so you never search your email for them. Lecture notes are dated files; homework gets one folder per assignment holding the prompt, your work, and what you submitted; exam preparation is built from the notes and past quizzes into a `study/` folder as the exam approaches. Finished courses move to an archive by term. The payoff: at any moment you can answer "what is due, what did we cover, and where is my submitted copy?" in seconds, and exam prep starts from organized material.

## Principles & why

1. **Same shape every course.** A predictable internal layout means no thinking about where a file goes; the muscle memory transfers across courses and terms.
2. **Time orders coursework.** Lectures, assignments, and exams happen in sequence; dated or numbered names make the folder read like the semester.
3. **Facts in one place.** Deadlines, weights, and links change; keeping them in the course README (and nowhere else) keeps one version true.
4. **Keep what you submitted.** The prompt, your work, and the submitted copy for each assignment are evidence of what was asked and what you did; grade disputes and later reference both need them.
5. **Study material is derived.** Cheatsheets and summaries are made from lecture notes and homework, and rebuilt each term; they don't replace the source notes.
6. **Archive by term, not by deletion.** Old courses are cheap to keep and often useful later (prerequisites, portfolios, interview prep); moving them out of the active folder keeps the present uncluttered.

## When to use

- **Students at any level** taking several courses per term.
- **Self-directed learners** following online courses or books with lectures and exercises.
- **Instructors and teaching assistants** organizing their own copies of course materials.
- **Anyone keeping a learning record** for later reference or a portfolio.

## When NOT to use

- **Long-term knowledge building across courses.** Course folders hold course material; durable ideas that connect across subjects belong in a linked note system (see `evergreen-notes` or `zettelkasten-classic`).
- **Group projects with their own repositories.** Keep the project in its own repository (see `project-archive`) and link to it from the course README.
- **Documents the institution controls** (grades, official records). Keep them where the institution provides them; copy only what you need.
- **One-off workshops.** A single folder of notes is enough.

## Tree diagram

```
school/
├── 2026-fall/
│   └── cs-101/
│       ├── README.md                     ← instructor, schedule, weights, deadlines, links
│       ├── syllabus.pdf
│       ├── notes/
│       │   ├── 2026-09-08-lecture-01-introduction.md
│       │   └── 2026-09-10-lecture-02-recursion.md
│       ├── readings/
│       │   └── 2026-09-08-chapter-1-summary.md
│       ├── homework/
│       │   ├── hw-01/
│       │   │   ├── prompt.pdf
│       │   │   ├── work.md
│       │   │   └── submitted.pdf
│       │   └── hw-02/
│       ├── quizzes/
│       │   └── quiz-01.md
│       ├── exams/
│       │   ├── midterm/
│       │   └── final/
│       ├── project/
│       └── study/
│           └── midterm-cheatsheet.md
└── archive/
    └── 2026-spring/
```

## Naming rules

- **Term folders** are `YYYY-season` (`2026-fall`, `2027-spring`), which sorts chronologically and reads clearly.
- **Course folders** are the course code in lowercase kebab-case (`cs-101`, `math-2210`), optionally with a short slug (`cs-101-intro`), consistent across terms.
- **Lecture notes** are `YYYY-MM-DD-lecture-NN-topic.md` (see `iso-date-formats`); the number matches the course's lecture numbering if it has one.
- **Assignments** are `hw-NN/`, `quiz-NN`, `midterm/`, `final/`, `project/`, numbered with zero-padded two-digit sequence numbers.
- **Inside an assignment**: `prompt.*` (what was asked), `work.*` (your working), `submitted.*` (the exact copy you handed in), and `feedback.*` (returned comments).
- **Study material** is named for its exam (`midterm-cheatsheet.md`), so it is obviously disposable after the exam.

## Worked example

A new term starts with four courses, and last term's files are still scattered across a `Documents/` folder and downloaded PDFs.

1. Create `school/2026-fall/` and archive last term by moving it to `school/archive/2026-spring/` (or keep it as `2026-spring/`; the point is one folder per term).
2. For each course, copy the template: `README.md`, `notes/`, `readings/`, `homework/`, `quizzes/`, `exams/`, `project/`, `study/`.
3. Fill the README on day one from the syllabus: instructor and office hours, meeting times, grading weights, exam dates, textbook, and links to the course site and discussion forum. Put deadlines in your calendar too.
4. Take lecture notes in `notes/2026-09-08-lecture-01-introduction.md`. After each lecture, add one line at the top: what the main idea was, and what you didn't understand.
5. For each assignment, make `homework/hw-01/`, save the prompt as soon as it's released, work in `work.md`, and store the exact submitted file as `submitted.pdf`.
6. A week before an exam, build `study/midterm-cheatsheet.md` from the lecture notes and the homework mistakes; note weak topics and do practice problems.
7. At term end, add a short retrospective to each README (what worked, what to reuse), then move the term to `archive/`.

Any question about the semester (what was due, what was covered, what I turned in) is answerable from one folder.

## Anti-patterns

- **Filing by file type across courses** (`all-pdfs/`, `all-slides/`). You always look for material by course and date, not by file extension.
- **Scanning or renaming later.** Files named `document (3).pdf` cost far more to fix at midterm time; name on save.
- **Only keeping the submitted copy** (or only the working file). Keep the prompt, your work, and the submitted version.
- **Course facts scattered** across email, the LMS, and notes. Put them in the README once.
- **Copying lecture slides as notes.** Slides are provided material (keep them in `readings/` or `slides/`); your notes are your own words and questions.
- **Never archiving.** The active folder grows until finding the current course is as hard as before.
- **Reusing old cheatsheets blindly.** They're derived from a different term's emphasis; rebuild.

## Scaling & failure modes

- **Many courses per term**: the identical shape is what keeps it manageable; add a term-level `README.md` with the deadline calendar across courses.
- **Multi-year programs**: archive by term, and keep a program-level `index.md` listing courses with links to their retrospectives; useful for prerequisite refreshers and applications.
- **Large file sets** (lecture videos, datasets): store outside notes or use pointers (see `large-files-and-binary-assets`); keep the folder text-first.
- **Shared materials** (group notes, class wiki): link to the shared source rather than copying; keep your own notes separate.
- **Version control**: putting notes in git helps with history and sync, but keep large binaries out.
- **Long-term value**: for concepts you want to keep beyond the exam, write atomic notes in a separate note system and link back to the lecture.

## Variants

- **Term-first** (this guide): `school/<term>/<course>/`, best when the calendar drives your work.
- **Course-first**: `courses/<course>/<term>/`, better for repeated or multi-term courses.
- **Digital notebook per course**: one file per course with dated headings; fine for short courses.
- **Zettelkasten-style**: lecture material feeds permanent notes in a separate system; the course folder holds only logistics and submitted work.
- **Instructor layout**: `course/lectures/`, `course/assignments/`, `course/exams/`, `course/handouts/`, with solutions kept separately.

## Adoption checklist

- [ ] Every course folder has the same subfolders and a filled README.
- [ ] Lecture notes and assignments are named with dates or numbers that sort in order.
- [ ] Each assignment folder holds the prompt, your work, and the submitted copy.
- [ ] Deadlines are in the README and in your calendar.
- [ ] Study material is derived from notes and is dated to its exam.
- [ ] The finished term is archived with a short retrospective.

## Real-world projects using this

- **Cornell note-taking system** (Walter Pauk) and similar methods describe how to structure the *content* of lecture notes; this guide organizes the *files*.
- **Johnny.Decimal** users often adapt numbered categories for school folders; see `johnny-decimal` for that variant.
- **University learning-center guides** (many publish "organizing your course materials" pages) recommend the same per-course, per-week structure.
- **Open courseware** such as MIT OpenCourseWare organizes materials by lecture notes, assignments, exams, and readings, which is the same set of categories used here.

## Migration & references

- **From a flat `Documents/` folder:** create the term and course folders, then move files by course using search on names and dates; delete duplicates only after checking.
- **From an LMS-only workflow:** download syllabus, prompts, and returned feedback into the course folders at the end of each term, before access ends.
- **To a linked note system:** keep the course folder for logistics and submissions, and copy durable ideas into atomic notes that link back to the lecture note.
- **References:**
  - `principles/iso-date-formats/` for dated filenames.
  - `principles/status-based-organization/` and `files/project-archive/` for archiving.
  - `notes/daily-weekly-notes/` for a daily log that can link to lectures.
  - `notes/literature-review-structure/` for readings-heavy graduate courses.
