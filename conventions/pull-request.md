### Introduction to Pull Requests:
Explanation of pull requests and their role in the version control process.
If all collaborators are admins on the repository, the process of creating and merging pull requests might vary slightly compared to when there are designated reviewers or maintainers. Here's how the pull request workflow typically works in such a scenario:

### 1. Creating Feature Branch:
Practice lean branching, where each team member works on a separate feature branch for new tasks and will merge changes directly into the main branch.

   - Each collaborator creates a feature branch from the main branch where they implement their changes or additions.
  
### 2. Work on Feature Branch

   - Collaborators work independently on their respective feature branches, implementing the required changes or additions, and running tests and formaters.
  
### 3. Pushing Changes to Feature Branch

   - Once a collaborator completes their work on a feature branch, they push their changes to the remote repository ONLY.
  
### 4. Pull Request Creation

   - Since all collaborators are admins, they have the privilege to directly create pull requests from their feature branches to the main branch without needing approval from other reviewers. **However this should be done by whoever is assigned to do so from the team**.
  
   - The main branch settings can be found `settings > code and automations > Branches` with the options selected as follows:
     1. require a pull request before merging
     2. require approvals
     3. Do not allow bypassing the above settings
   
   - Always include a link to the ticket in the pull request description.
  
   - Keep pull requests as small as possible. This wil make reviewing easier, less occurence of getting merge conflicts.

### 5. Review Changes

- The person who is assigned to review the changes ensures that the project's standards and requirements are met, including providing feedback, asking questions, and suggesting improvements in the comments section. For this look at the [project-plan](project_plan.md) and also [specs](specification.md)
   
### Merge Strategy:
Explanation of the merge strategy used, ensuring that changes are merged into the main branch via pull requests.