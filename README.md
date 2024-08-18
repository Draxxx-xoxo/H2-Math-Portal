# H2 Math Portal

## How to login
### __User__
- Email: student@example.com
- Password: ExampleStudent

### __Admin__
- Please ask me for the email and password if you would like to test out admin


## Inspiration

I wanted a way for students to practice Mathematics questions while also having some fun and a way to compete with their peers. This way it is more engaging and students can learn through practice. This also allow teachers to create quizzes for students to practice and also to see how well they are doing.

## What it does
This website allows students to practice their H2 Mathematics questions. Quizzes are created by teachers with different questions. The website will generate random values for each question and the user can input their answer. The website will check if the answer is correct. The website also has a leaderboard to show students with score. The website also has an admin page where the admin can add new questions, add new quizzes for students, and add new users to the portal. 

## How it's built

## Tools and APIs used
- [Supabase](https://www.supabase.com) (PostgreSQL)
- [WolframAlpha](https://www.wolframalpha.com) (API)
- [Vercel](https://vercel.com/draxxxxoxos-projects) (Hosting)
- [Sentry](https://sentry.io) (Error Tracking)
- [Resend](https://resend.io) (Email Verification)
- [Mathjax](https://www.mathjax.org) (Mathematical Equations)
- [Tailwind CSS](https://tailwindcss.com) (CSS)
- [JQuery](https://jquery.com) (JavaScript)

It is build on the Flask framework with the following python libraries: Supabase, Numpy, Sentry, Sympy, Pytz, Requests, Antlr4-python3-runtime, Py_asciimath. I have used an open-source PostgreSQL database provided by Supabase to store the data and authenticate users. The website is hosted on Vercel. Resend is also used for email verification using the Supabase API. The frontend website is built with HTML with Jinja template engine, CSS, and JavaScript. Frotend APIs used are Mathjax, Tailwind CSS and JQuery.

### User Authentication
The user authentication is done using the Supabase API. The user can log in, and log out, reset their passwords and change their email. Access Tokens and Refresh Tokens which are JWT token are used to authenticate the user. Email verification is also done using the Supabase API and sent by Resend.

### Leaderboard
The leaderboard is updated everytime a user answers a question. The leaderboard is sorted by the score of the user.

### Quiz Generation
The quiz generation is done by generating random values for each question. The random values are generated using numpy. The random values are then stored in the database and retrieved everytime the user answers the question. 

### Quiz Page
For mathematical equations to be displayed on the website, mathjax is used to formate mathematical symbols and vectors. There are also buttons that will auto fill ASCIImath symbols into the input box and will render in realtime to see what the equation would look like. There is also a time that will check with the db time and the server time to determine the time reamining.

### Answer Checking
The answer checking is done by using the WolframAlpha API, numpy and sympy. WolframAlpha API helps with answering differentiation and integration questions. Answers are then stored in the database and retrieved everytime it checks the answer. For indefinately integral questions, sympy is used to check the answer. For vectors question numpy is used to check the answer.

## Challenges encountered
- At the begining I had problems with the Supabase Authentication. Users were authenticated but the website would not redirect to the home page instead of the dashboard. To solve this I had to store the session in flask-sessions and set the session with Supabase every time the user enter a route that requires authentication.

- I had problems trying to solve integration and differentiation questions. I had to use the WolframAlpha API to solve the questions and since there is no direct way to check if the equation was correct, I had to parse through the API equation through sympy to change the equation to LaTeX for sympy to understand and then sub in a value to compare both answers.

- Another problem I had was using Mathjax to render mathematical. At first all my equations were rendering as LaTeX math symbols. I had to change the configuration of Mathjax to render ASCIImath symbols ,for better understanding.

- Trying to use Row Level Security in Supabase to only allow the user to see their own data was a challenge. I had to create a policy in the database to only allow the user to see their own data and ensure that the user was authenticated before they could see the data.

- Deploying to Vercel was also a challenge. As it does not naturally support python, I had to use a workaround by using a python serverless function to run the python code. 

## Accomplishments that I'm proud of
- I was able to use Supabase to authenticate users and store data in the database. 
- I was able to use the WolframAlpha API to solve differentiation and integration questions.
- I was able to use Mathjax to render mathematical equations.
- I was able to use Tailwind CSS to style the website.
- The website look complete and is functional.
## What I learned
I learned how to use Supabase to authenticate users and store data with Supabase. I also learned to use different APIs to achieve different functionality. WolframAlpha API to solve differentiation and integration questions. Mathjax to render mathematical equations and Tailwind CSS to style the website. I also learnt how to deploy a website on Vercel.

## What's next for H2 Mathematics Portal
I hope to add more questions to the portal and hopefully be able to implement this school wide for teachers to administer Pop Quizzes and there can be a daily task where students can do daily questions. I also hope that there could be a file upload option for students to upload their working to earn more points. There working would be chcek by teachers on the website. I also hope to add solutions where users can see why their answers were wrong.
