# Review of the paper

I'm reviewing the paper and providing feedback. Notice that, sometimes you may need to review this repository log file, memory, the .copilot-tracking folders, and the GitHub PR and Issues history to better understand what happened and also to refresh the evidence.

## 1. Review this fact: A six-week architectural demonstrator provides a motivating testbed: 183 pull requests merged  from 15 to 24 October 2026, 6:19:39 UTC, while the replacement remained unusable for the participant. 

This is not completely true, review the PR history, and the most important thing it's not the number of PRs but the full story, including how the epics and user stories were created. We generated agent-assisted research documents, BRDs, PRDs and ADRs, critiqued them using the Design Thinking coach, ran other DT techniques like what-if scenarios, user journey mapping and persona analysis. Then we created a few throw-away pilots and prototypes to better understand what we wanted to build. This accelerated the planning and documentation process, influencing how features were implemented and reviewed, there were long conversations, steering and decisions made between the agents and the user, that ended up in a long trail of context and helped another agent generate all the epics and user stories. In the theory, doing all this job should have accelerated the overall development process and improved the quality of the resulting features (this is what HVE promises), rather than merely increasing the number of merged pull requests. Yet, after some long autonomous sessions, the result was that the solution remained unusable for the participant, until he started providing feedback to refine and refactor the implementation.

Talking about the nr of pull requests or the dates in the abstract is a bit useless and does not bring anything to the point of the paper, which is to understand the dynamics of feature-driven decay and the role of agentic processes in shaping the development outcome.

## 2. No experiment results are reported.

This should be a TODO, not a statement in the paper, indicating that the experiment results are yet to be reported once the prospective runs and analysis are complete.

## 3. "The question arose during an Azure Master Architect (AMA) capstone"

Don't overemphasize the AMA capstone context in the abstract nor in the paper, we don't need all this specific dates and times, and, furthermore, as this is a work in progress project during the paper writing, the numbers we show there will be a moving target. Direct people to the repository for the most up-to-date information. Notice that this repository will be under embargo for a few days during the experiment run, after which the full history and context will be available for review again. Don't rely on the static numbers in the paper, and don't worry if the repository is temporarily unavailable, this is normal.

## 4. This, not that... What it is, what's not...

There are lots of sentences that sound AI generated, and one of the most common traits is that structure where you present a fact and then you negate proof or cause in some sentences like:

* Repeated failure is persistence, not proof that an earlier defect caused a distinct later one
* Arrows are possible state transfer, not measured error propagation
* This is a counterexample, not a test of the current autonomous roster
* Selected cohorts overlap; they are not independent studies or randomised repair conditions.
* Values and whiskers are transcribed, not fitted here.
* It motivates checking observable action outcomes, not a claim about coding consolidation or a controlled self-improvement intervention

And I don't say that these sentences are wrong, they just feel unnaturally defensive or hedged, which is a common trait in AI-generated text. Please detect these patterns and consider rephrasing them to sound more natural and assertive. You don't need to change them all, sometimes it makes sense to negate a fact, but be mindful of the overall tone and readability.

## 5. Capstone use case is not relevant

This sentence: "Case Study 48 supplies a fictional not-for-profit housing association, Zava North Homes, with about 60,000 homes." is not particularly relevant to the main focus of the paper. Consider explaining the exercise done for the capstone in a more abstract way without delving into specific fictional entities, names or numbers. The important parts here are the methodology, the type of analysis performed, how the solution was build using multiple agents and a coordinatero, and the insights gained, rather than the specific fictional context.

## 6. Specific dates on the capstone project are not important

ex: "from 11 September to 24 October 2026"

Avoid including exact dates for the capstone project in the paper. The focus should be on the methodology, analysis, and insights rather than the timeline. Specific dates are not critical to understanding the work and may become outdated or irrelevant as the project evolves. Details that may be important are the time spent on different phases of the project, the sequence of activities, and the overall duration without tying it to specific calendar dates.

## 7. Evidence on point 3.6

Review the evidence and summarize it again focusing on what's relevant for the main topic of the paper. The paper is not about the specific fictional entities, names, or numbers used in the capstone exercise, but rather about the methodology, analysis, and insights derived from the project that triggered this study. Later on we will have data from the actual experiment.

## 8. Review tables and figures and update what's relevant in the project

Review history, you may also check https://github.com/users/jmservera/projects/7/insights?period=1M

Check same than in point 7 in all the point 4. Don't go too deep on what happened with the project, we will dig deeper in the experiment when we have the data.

## 9. Overall review of all the formulas. 

Use the sympy, statistical-analysis, scientific-critical-thinking, and experimental-design skills to review all the formulas presented in the paper, ensuring their correctness, relevance, and alignment with the methodology and insights discussed.
