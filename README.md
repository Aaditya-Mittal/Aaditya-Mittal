<!--
  SETUP (two minutes)
  1. Find and replace @@GITHUB@@ with your GitHub username and @@LINKEDIN@@ with your LinkedIn slug.
     They only appear in links, never in images, so nothing breaks if you forget.
  2. Push this repo (it must be named exactly like your username), then run the "Profile cards"
     workflow once from the Actions tab. It fills in the live stats, languages, heatmap and snake.
-->

<div align="center">

<img src="assets/hero.svg" alt="Aaditya Mittal. Backend integrations, APIs and AI." width="100%" />

<br /><br />

<a href="https://www.linkedin.com/in/@@LINKEDIN@@"><img src="assets/btn-linkedin.svg" alt="Connect on LinkedIn" height="46" /></a>
<a href="mailto:aaditya.mittal111@gmail.com"><img src="assets/btn-email.svg" alt="Email aaditya.mittal111@gmail.com" height="46" /></a>
<a href="https://codolio.com/profile/Aaditya%20Mittal"><img src="assets/btn-codolio.svg" alt="Coding profile on Codolio" height="46" /></a>

<br /><br />

**Quick links**

[About](#about-me) &nbsp;|&nbsp; [Top project](#top-project) &nbsp;|&nbsp; [More work](#more-work) &nbsp;|&nbsp; [Tech stack](#tech-stack) &nbsp;|&nbsp; [Experience](#experience) &nbsp;|&nbsp; [Stats](#stats) &nbsp;|&nbsp; [Connect](#connect-with-me)

</div>

<br />

> [!NOTE]
> Open to **Software Engineer**, **Backend Engineer**, **AI Engineer** and **ML Engineer** roles. Feel free to connect.

<br />

<img src="assets/impact.svg" alt="All India Rank 1 at HackNow among 260+ teams. 500K+ tickets automated every year. 20+ developers use my dependency script daily. 12 integrations delivered. 700 coding problems solved." width="100%" />

<br />

## About me

I wrote my first program in 9th standard. It was meant to print the Fibonacci series. The computer disagreed with my ideas, so I changed something, ran it again, changed something else, ran it again.

That loop never left. Today I work as an Analyst on enterprise platforms, building backend integrations and APIs on ServiceNow. Most of it is getting systems that don't always agree to agree, and I like it for exactly that reason. I am moving toward AI and software engineering, with ServiceNow as the entry point and not the destination.

**Education:** B.Tech in Computer Science (AI & ML), JECRC University, CGPA 9.49
<br />
**Certified:** ServiceNow CSA, CAD, CIS-DF, CIS-ITSM, plus NVIDIA AI for Anomaly Detection
<br />
**Outside code:** I taught myself chess from a rulebook and a Kasparov book, and I still play every day.

```js
const aaditya = {
  role: "Analyst, backend integrations & APIs",
  platform: "ServiceNow",
  languages: ["Python", "C++", "JavaScript"],
  building: ["FastAPI services", "LLM apps"],
  motto: "I stop at \"I understand why\", not at \"it works\".",
};

while (!solved) {
    try_again();
}
```

<br />

## Top project

### Social Media Engagement Tracker

My hackathon-winning ServiceNow app, and the reason I got to work on real integrations in the first place. It pulls Facebook and Instagram data every 15 minutes, scores the sentiment of what people say, clusters their comments, and raises an alert the moment a PR crisis starts to build. Weekly and monthly reports go out on their own.

I decided the whole build and wrote the ingestion layer, tuned to API limits so it scales to 10,000+ interactions per account per day. It won **All India Rank 1** at the ServiceNow x Deloitte HackNow, among 260+ teams.

<img src="https://img.shields.io/badge/ServiceNow-81B5A1?style=flat-square" alt="ServiceNow" />
<img src="https://img.shields.io/badge/Workflow%20Studio-1F2937?style=flat-square" alt="Workflow Studio" />
<img src="https://img.shields.io/badge/Predictive%20Intelligence-1F2937?style=flat-square" alt="Predictive Intelligence" />
<img src="https://img.shields.io/badge/UI%20Builder-1F2937?style=flat-square" alt="UI Builder" />
<img src="https://img.shields.io/badge/Graph%20API-1F2937?style=flat-square" alt="Graph API" />

```mermaid
flowchart LR
    A["Facebook Pages<br/>Instagram Graph API"] -->|every 15 min| B["Scheduled ingestion<br/>7 Script Includes"]
    B --> C[("ServiceNow tables")]
    C --> D["Sentiment<br/>Predictive Intelligence"]
    C --> E["Comment clustering"]
    D --> F["Workflow Studio<br/>crisis alerts and reports"]
    E --> G["UI Builder dashboard"]
    F --> G
```

<br />

## More work

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>AI Website Summarizer</h3>
      <p>Paste a URL and watch the summary stream in as it is written. Playwright renders the page, so JavaScript-heavy sites work too. Gemini 2.5 Flash does the reading.</p>
      <p>
        <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square" alt="FastAPI" />
        <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat-square" alt="Playwright" />
        <img src="https://img.shields.io/badge/Gemini%202.5%20Flash-8E75B2?style=flat-square" alt="Gemini 2.5 Flash" />
      </p>
      <p><a href="https://github.com/@@GITHUB@@?tab=repositories&q=summarizer">Source</a></p>
    </td>
    <td width="33%" valign="top">
      <h3>Anime Face Generator</h3>
      <p>A DCGAN trained from scratch on 10,000 anime faces for 1,000 epochs. Co-authored the paper presented at I-LIPS 2025.</p>
      <p>
        <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square" alt="PyTorch" />
        <img src="https://img.shields.io/badge/PyTorch%20Lightning-792EE5?style=flat-square" alt="PyTorch Lightning" />
      </p>
      <p><a href="https://github.com/@@GITHUB@@?tab=repositories&q=dcgan">Source</a></p>
    </td>
    <td width="33%" valign="top">
      <h3>IAESTE chapter website</h3>
      <p>The chapter site was broken, so I proposed a plan and rebuilt it in React and Tailwind CSS. It now scores 91 on SEO.</p>
      <p>
        <img src="https://img.shields.io/badge/React-20232A?style=flat-square" alt="React" />
        <img src="https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat-square" alt="Tailwind CSS" />
      </p>
      <p><a href="https://github.com/@@GITHUB@@?tab=repositories&q=iaeste">Source</a></p>
    </td>
  </tr>
</table>

<details>
<summary><b>Under the hood: AI Website Summarizer</b></summary>

<br />

```mermaid
flowchart LR
    U["URL"] --> API["FastAPI"]
    API --> PW["Playwright<br/>renders the page"]
    PW --> BS["BeautifulSoup4<br/>cleans the text"]
    BS --> G["Gemini 2.5 Flash"]
    G -->|streamed| UI["Summary, as it is written"]
```

</details>

<br />

## Tech stack

<table>
  <tr>
    <td width="170"><b>Languages</b><br /><sub>Python, C++, JavaScript, HTML, CSS</sub></td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=py,cpp,js,html,css&theme=dark" />
        <img src="https://skillicons.dev/icons?i=py,cpp,js,html,css&theme=light" alt="Python, C++, JavaScript, HTML, CSS" />
      </picture>
    </td>
  </tr>
  <tr>
    <td><b>Backend</b><br /><sub>FastAPI, Node.js, Express, REST APIs</sub></td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=fastapi,nodejs,express&theme=dark" />
        <img src="https://skillicons.dev/icons?i=fastapi,nodejs,express&theme=light" alt="FastAPI, Node.js, Express" />
      </picture>
      &nbsp;<img src="https://img.shields.io/badge/REST%20APIs-7C3AED?style=for-the-badge" alt="REST APIs" />
    </td>
  </tr>
  <tr>
    <td><b>Data</b><br /><sub>MongoDB, MySQL, PostgreSQL</sub></td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=mongodb,mysql,postgres&theme=dark" />
        <img src="https://skillicons.dev/icons?i=mongodb,mysql,postgres&theme=light" alt="MongoDB, MySQL, PostgreSQL" />
      </picture>
    </td>
  </tr>
  <tr>
    <td><b>AI and ML</b><br /><sub>PyTorch, LLM apps</sub></td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=pytorch&theme=dark" />
        <img src="https://skillicons.dev/icons?i=pytorch&theme=light" alt="PyTorch" />
      </picture>
    </td>
  </tr>
  <tr>
    <td><b>Frontend</b><br /><sub>React, Tailwind CSS</sub></td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=react,tailwind&theme=dark" />
        <img src="https://skillicons.dev/icons?i=react,tailwind&theme=light" alt="React, Tailwind CSS" />
      </picture>
    </td>
  </tr>
  <tr>
    <td><b>Platform</b><br /><sub>ServiceNow, Workflow Studio, Scripted REST APIs</sub></td>
    <td><img src="https://img.shields.io/badge/ServiceNow-81B5A1?style=for-the-badge" alt="ServiceNow" /></td>
  </tr>
  <tr>
    <td><b>Tools</b><br /><sub>Git, GitHub, Postman, Vercel, Linux, VS Code</sub></td>
    <td>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=git,github,postman,vercel,linux,vscode&theme=dark" />
        <img src="https://skillicons.dev/icons?i=git,github,postman,vercel,linux,vscode&theme=light" alt="Git, GitHub, Postman, Vercel, Linux, VS Code" />
      </picture>
    </td>
  </tr>
</table>

<br />

## Experience

| When | What | Highlights |
| :-- | :-- | :-- |
| Jul 2026 to now | **Analyst**, enterprise platforms (ServiceNow) | Own and extend backend integrations end to end: design docs, build, testing, UAT and handover. Took over integrations from other developers through knowledge transfer. |
| Before full time | **Intern**, ServiceNow integrations | Built 6 integrations and the automation behind 500K+ tickets a year. Converted to full time. |
| 2025 | **Remote research intern**, Iran University of Science and Technology (IAESTE) | Evaluated bot-detection models (BotRGCN, BotHunter) on Twitter profiles, in a team of five across three countries. |
| 2023 to 2025 | **IAESTE LC JECRC**, Head of IT-DA and Deputy Head, Incoming | Rebuilt the chapter website. Digitized intern onboarding and cut the time per intern by about 25 to 30 percent. |
| 2023 to 2024 | **GDSC JECRC**, AI & ML core team | Anchored an orientation of about 200 people and taught Python to 25+ juniors. |

<br />

## Stats

<a href="https://codolio.com/profile/Aaditya%20Mittal"><img src="assets/codolio.svg" alt="Codolio: 700 problems solved, 26 contests, longest streak 177 days" width="100%" /></a>

<br />

<div align="center">

<table>
  <tr>
    <td><img src="assets/stats.svg" alt="GitHub statistics" width="100%" /></td>
    <td><img src="assets/langs.svg" alt="Top languages" width="100%" /></td>
  </tr>
</table>

<img src="assets/heatmap.svg" alt="Contribution heatmap for the last year" width="100%" />

<br /><br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/github-snake-dark.svg" />
  <img src="assets/github-snake.svg" alt="Contribution snake" width="100%" />
</picture>

</div>

<sub>The GitHub cards are generated by [`scripts/generate_stats.py`](scripts/generate_stats.py) through a scheduled GitHub Action, with no third-party stats service involved. The Codolio numbers are as of October 2026.</sub>

<br />

## Right now

- Taking more integrations from design to production, and writing the docs so the next person has an easier time than I did.
- Building LLM-powered apps in Python and FastAPI. The summarizer was the first. It will not be the last.
- Getting into open source. First stop: [ServiceNow/PySNC](https://github.com/ServiceNow/PySNC), a Python client for the ServiceNow Table API.
- Solving a problem a day in C++, when the day allows.

<br />

## Connect with me

<div align="center">

### Recruiter or engineer with a hard problem? Feel free to connect.

<a href="https://www.linkedin.com/in/@@LINKEDIN@@"><img src="assets/btn-linkedin.svg" alt="Connect on LinkedIn" height="46" /></a>
<a href="mailto:aaditya.mittal111@gmail.com"><img src="assets/btn-email.svg" alt="Email aaditya.mittal111@gmail.com" height="46" /></a>

</div>
