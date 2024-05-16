# Pull requests

## Introduction to Pull Requests

Explanation of pull requests and their role in the version control process.
If all collaborators are admins on the repository, the process of creating and merging pull requests might vary slightly compared to when there are designated reviewers or maintainers. It could cause issue with missing files and or settings from tasks done by other collaborators. This how we will use our pull rrequests:

## 1. Creating Feature Branch

Practice lean branching, where each team member works on a separate feature branch for new tasks and will merge changes directly into the main branch.

- Each collaborator creates a feature branch from the main branch where they implement their changes or additions.

## 2. Work on Feature Branch

- Collaborators work independently (or in pairs) on their respective feature branches, implementing the required changes or additions, and running tests and formaters.

## 3. Pushing Changes to Feature Branch

- Before committing the changes githooks precommit will run to check al linting and formatting is done
- Once a collaborator completes their work on a feature branch, they push their changes to the remote repository on the feature branch.

## 4. Pull Request Creation

- All collaborators will be able to apprve/review pull requests except their own

- The main branch settings can be found `settings > code and automations > Branches` with the options selected as follows:

  1. Require a pull request before merging
  2. Require approvals
  3. Do not allow bypassing the above settings

- Always include a link to the ticket in the pull request description.

- Keep pull requests as small as possible. This wil make reviewing easier, less occurence of getting merge conflicts.

## 5. Review Changes

- The person who is assigned to review the changes ensures that the project's standards and requirements are met, including providing feedback, asking questions, and suggesting improvements in the comments section. For this look at the [project-plan](project_plan.md) and also [specs](specification.md)

## Merge Strategy

- Once reviews are approved, the reviewer will merge the changes to main.

## Deployment

- Once changes are merged to main, the CI pipeline will run automated tests and checks, before merging the changes to the deployment branch. The CD pipepline will deploy the updated code to the live infrastructure.
