### ERP Portal Automation

#### This is a simple script to automate the process of logging into the ERP portal and doing stuff.

- There are two scripts currently, one to check pending grades result and the other to register for a course which has some upper cap ( first come first serve ).

- If you want to deploy this, one way is to package as a lambda and run on aws, but it gets tricky with chromedriver and selenium, although doable but the docker image size is huge.
So instead i am running it as a cron job on a linux server on ec2 instance.

- send-email is the lambda function that uses amazon SES to send emails for events. As STMP traffic is trottled on a ec2 instance, so i made an api using api gateway with lambda proxy integration 
to trigger this lambda and send emails.

set username and password env var in .env

So it looks like this : 

EC2 instance -> API Gateway -> Lambda -> SES