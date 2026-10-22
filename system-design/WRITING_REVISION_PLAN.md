# Current writing revision: Units 3 and 4

Completed on **22 October 2026**. The user narrowed the work to these two units and made the `ncert-style-writing` approach mandatory: engaging, very simple language, with the necessary explanations before relying on unfamiliar terms. Unit 1 is the reference.

## What changed

Unit 3 follows a browser opening the task application. It shows URL parts and an HTTP request, a packet reaching a listening program, a missing TCP byte range, DNS caching, certificate checks, the TCP handshake, NAT return mapping, and a request whose reply is lost. Operation identity is distinguished from the created task's identity.

Unit 4 follows uploaded files. It explains process/thread and stack/heap meanings before using them, follows a task through an event loop, reproduces a lost counter update, traces lock and condition-variable operations, and shows publication, backpressure, and cancellation. The worker pseudocode declares its queue acceptance rule and cleanup, with the example's limits stated before or beside it.

All 34 lessons and eight chapter introductions were rewritten. Related traces, captions, reference summaries, code explanations, queue instructions, and 22 assessments were revised. Plain-language section headings replace topic-list headings in these lessons; syllabus items and stable links remain. The memory layout comes after stack/heap explanation, and an unrelated URL-shortener diagram was replaced by the task-list request. Unit-level advanced questions occur at the end of these units rather than after every chapter.

The lesson prose changed from 6,435 to 5,528 words. The aim was to remove repeated advice and use the space for missing steps, rather than target a uniform length. Important technical conditions remain beside the claims they qualify.

## Scope and verification

All other 91 generated chapter panels match baseline commit `3721887` byte for byte, including Unit 1. Non-target lesson, guide, reference-summary, assessment, and worked-code data are unchanged. All assessment kinds and IDs remain.

The complete build, executable checks, browser suite at five widths, and scoped preservation checks pass. Desktop/mobile readings and representative PDF pages were inspected. The refreshed complete PDF has 1,070 tagged A4 pages. It exports the current book; only the two target units' chapter content changed in this pass. See [QA.md](QA.md).
