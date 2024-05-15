# Code Reviews

## Introduction to Code Reviews

This section details the steps involved in reviewing code within a submitted pull request. Refer to the separate [pull request](pull-request.md) process document for information on submitting PRs.

## PR Assignment

Upon PR submission assign the code review the team member who is working solo for that day as per the calender. If you are working solo assign to another member of the team and ensure to rotate assignees.

## Review and Feedback

### 1. Code Clarity

- Well-structured and easy to understand code.
- Meaningful variable and function names that reflect their purpose.

### 2. Implementation

- Does the new code do what it was designed to do? 
- Does it reflect the requirements of the linked issue? 
- Does it handle potential edge cases correctly?

### 3. Style and consistency

- Does it follow a consistent style and pattern within the project?
- Ensure all code is pep8 compliant, Refer to [PEP 8](https://pep8.org/) guidelines for details.

### 4. Maintainability

-  How easy it is to modify, integrate, or extend with the existing codebase in the future.

### 5. Documentation

- Ensure all functions are documented using [docs-and-comments](docs-and-comments.md) as reference.

### 6. Testing

- All Python code should be thoroughly tested.
- Test coverage should exceed 90%.
- Are clear and well-organised tests written?
- Do they cover different scenarios effectively?
- Are mocking frameworks used to isolate dependencies during testing?

### 7. Frame feedback as requests, not commands

- Avoid imperative language; instead, invite discussion and collaboration.
- Use phrases like 'Could you consider...' or 'Would it be possible to...' when suggesting changes.
- Keep feedback constructive and supportive.

## Merge Strategy

- Once reviews are approved, the reviewer will merge the changes to main.

## Deployment

- Once changes are merged to main, the CI pipeline will run automated tests and checks, before merging the changes to the deployment branch. The CD pipepline will deploy the updated code to the live infrastructure.
