<h1>Launch a static website using AWS S3 and boto3.</h1>
<h2>How This Program Works.</h2>
  <h3>1:- Creates a S3 Bucket. User can pass the bucket name at the initial configuration, otherwise the default name for the bucket will be used.<h3>
  <h3>2:- Set the Website Configuration object to enable the static hosting. Program is having a property WebsiteConfiguration IndexDocument set as 'index.html'. Same can be done for handling the web page error by setting ErrorDocument.
  <h3>3:- Set the Bucket policy to Public Read Objects. To host a static website, we have to make sure that Bucket Policy allows any one from the internet to access the                   web content. <h3>
  <h3>4:- Once All of the above configuration succesfully got executed, our website content will be automatically uploaded to this S3 Bucket from the specified     directory.
  <h3>5:- Once Website content are uploaded, program will throw the output of URL, this URL can be use to access the static website.</h3></br>
    
    
    
    
 ![alt text](https://github.com/shivanis400/ProgrammingCPP/blob/master/static-log.JPG?raw=true)</br>
 </br>
 
 

 
 <h1>We can also launch a static website using AWS cloudformation and other tools</h1>
 <h2>How Clouformation Template Would Work.</h2>
  <h3>1:- Creates a S3 Bucket. User can pass a bucket name as a parameter. If no bucket name is passed, the default bucket name  "edcast-static-webhost" will be used.
  <h3>2:- This Bucket is having a property WebsiteConfiguration index or default page as 'index.html', which enables static web hosting using this bucket url.
  <h3>3:- Since we have enabled static web hosting in previous step, we have to make sure that Bucket Policy allows any one from the internet to access the web content. So i have enabled get-object action in my s3 bucket. 
  <h3>4:- Once above configuration are successfull, now we have to upload the website content to the bucket.</h3>
          <h3> Since we cannot copy from local computer to CloudFormation. Reason is, CloudFormation template runs on remote systems so it does not know how to connect with our your local machine. So making this process with no interventaion we have 3 choices.</h3>
           
         1:- We can upload our website content to a version control or any other HTTP/s URL to pull the file and put it in the bucket. 
         2:- We can use AWS cloudformation macros to perform custom processing on template, in this way we can copy the website
             from local to the s3 bucket.
         3:- Setup the whole configuration using Cloudformtion template and then using aws s3 cp command to copy the content to
             the s3 Bucket. The template i have uploaded is using AWS cloudformation Macro.
    
  <h3>5:-  On Sucessfull deployment of our Cloudformation stack using Option 2, we can see the stack output like WebsiteURL, Bucket Name.</h3>
