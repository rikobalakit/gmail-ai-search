# gmail-ai-search
AI Prompts to search your Gmail inbox *smartly*. A project for me to learn AI/ML while I'm between jobs.

This is an application designed to help search for a type of email using AI prompts instead of classic search queries.
I started this project when I was frustrated about trying to search for a type of email, such as "Music software and audio sample purchases and downloads, excluding promotional letters", or "Job search correspondence excluding automated 'Thank you for submitting your application, we will get back to you shortly" type emails. This was after I became comfortable with using ChatGPT in my daily workflow as an alternative search engine.

I have also heard the praises sung about the use of ChatGPT for helping design the architecture of a project, generate tutorials for workflows, and decide on which technologies to use given various contexts. This will be my first time using AI to assist me in the architecture of a project- more in the form of me bouncing off ideas and verifying if they make sense, and presenting some choices for parts of the stack, me making a choice based off my thoughts on each part of the stack, and asking ChatGPT to verify my decision and points. I did not want ChatGPT to design the entire project for me, but rather to act as an assistant to make sure my "architect" senses are being developed- I still want to drive many of the decisions for it.

Although I have learned there exist tools that can do what I think I want this application to do (namely, Copilot + Outlook), I wanted to write a version of this myself while I am seeking employment:
 - I have no income so I do not want to spend money on another subscription.
 - I wanted to familiarize myself with using AI tools and libraries since they are very "hot" on the job market.
 - I wanted to refamiliarize myself with Python, which I have not used since my college years, and is also very popular on the job market.
 - I am confident/naive enough to think I can write a better tool than Microsoft.
 - I'm bored and need purpose in my life so I don't just play video games and whine about the job market all day.
 - I wanted to familiarize myself with what the hell a "DevOps" is.
 - I wanted to "test" ChatGPT (model 4o) to see if it's really a very useful tool, or if it will lead me astray with insanely convincing hallucinations of an android that does not dream of electric sheep.

# Stack

Here is the overall high level stack:
 - Python language
 - Docker for deployment
 - GitHub for repository
 - GitHub Actions for, to be honest, I don't quite know what it does yet, but I asked ChatGPT to recommend another "devopsy" thing to tack on to this project.
 - Flask, eventually, for the web server
 - PostgreSQL for the database
 - Google Mail API
 - No idea which AI model/library/whatever I'll be using yet, I'm trying to hello-world this and the Gmail API first.

# Why I picked this stack

So here are the choices for my tech stack:
Language: I wanted to decide between C#, C++, and Python. These are the top three languages I am most familiar with.
 - Python seemed to have the most support, by far, for AI/ML tools and libraries, and possibly the most jobs on the market today.
 - C++, I am trying to become more proficient in (for Unreal and Embedded Systems), but feels inappropriate for this use case.
 - C#/.NET has plenty of use in web dev stacks, but I already feel very proficient in it that I don't need to "brush up" on it for this.

ChatGPT verified my intuitions with Python. So lets go with Python.

Deployment: I immediately just went to Docker since it's on all the job applications.
 - Docker: Like I said, EVERYONE seems to use it. I didn't even ask ChatGPT for alternatives here lol.

Repository & "Pipelines"/"Runners": So I know what a repo is, honestly I think I sort of get what a runner does (tests and deployment? I'm reminded of TeamCity). I figured since they live on Github and Gitlab, it's a bit of a two-fer deal.
 - Github Actions, I already have an account with most of my projects on, and companies ask for my Github link a lot more than a general personal repo or Gitlab.
 - Gitlab CI/CD, I have an empty gitlab account, and CI/CD isn't as cool sounding as "Actions".

ChatGPT says that they're kind of equally suited for my project, and recommended Github if I want to be lazy and stick with a familiar tool and company. So lets go with Github and Github Actions.

Web Server: I'm just going with Flask, I've used it before and the goal of this project isn't to familiarize myself with frontend web dev (yet). It'll probably be fairly minimal. Classic Twitter Bootstrap too because I'm already familiar with it.
- Flask: Yep, just good ol simple Flask. Already familiar with it, probably easier integration with the Python ML/AI stuff, and more Python practice.

ChatGPT says Flask is okay. Let's go with Flask.

Database: I've used MySQL. I've used SQLite. I haven't used PostgreSQL. MongoDB didn't feel appropriate for this project. Let's see...
- SQLite: I know this is a terrible choice for massive databases, and my 60k email Gmail account is probably 1-2GB of raw text. ChatGPT agreed, SQLite will be a terrible bottleneck. Nope.
- MySQL: ChatGPT says it'll be appropriate, and it's standard. I'm already familiar with it.
- PostgreSQL:  ChatGPT says it's uh, "more advanced" and probably more performant. Never used it before, but the syntax looks similar enough to MySQL.

I begrudgingly went with PostgreSQL. I guess it's another thing to add to my resume. I don't even know why I'm upset about it (it's my choice after all).

Mail API: I only use Gmail, so I can only use Gmail for this.
- Gmail: I already use this

Easy. We're going with GMail.

AI/ML Model: I'll cross that bridge when we get there, let's hello world this.
