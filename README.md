<!DOCTYPE html>
<html>

<body>

<h1>Cloud Computing Project</h1>
<h2>Deploy a Streamlit app with Docker using AWS EC2 and as services Docker Swarm, Apache, Docker Stack, PostgreSQL, and Redis.</h2>
<h2>The Application</h2>
<p>For the purposes of this project, I used a Streamlit application that provides detailed information on Yu-Gi-Oh! cards from 2000 to the present.</p>
<p>This application is designed to understand which cards are the most appreciated, viewed, banned, and criticized for their power or rarity.</p>

<h2>What are the steps?</h2>
<p>The idea is to deploy the application using Amazon Web Services (AWS) and its cloud-based products.</p>
<p>To have a functioning application in the cloud, these are the steps I followed:</p>
<ul>
<li>Creation of a Docker image of the application and its dependencies.</li>
<li>Creation of virtual instances with AWS EC2.</li>
<li>Creation of a Docker Swarm composed of one manager and three worker nodes.</li>
<li>Creation of PostgreSQL, Apache, and Redis services.</li>
<li>Creation of a Docker Stack so that no stack runs on the Manager node.</li>
<li>Storage on Docker Hub.</li>
</ul>
<br> </br>
<h2>Creation of a Docker image of the application and its dependencies.</h2>
<p>
The creation of the docker image was applied to create everything needed to run the software, meaning code, libraries, variables; that is, to distribute that package and run the software in a containerized environment.
Before creating the Docker image, I first created a text file named “requirements.txt” where all the libraries with their specific versions are included, both for the descriptive analysis of the data and for the creation of the streamlit application.
</p>

<p>After creating the “requirements.txt” file, I went on to create the Docker file using these codes:</p>

<pre>
<code>
# Use a Python base image
FROM python:3.8

# Set a working directory
WORKDIR /app

# Copy necessary files into the image
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8501 (Streamlit's default port)
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]
</code>
</pre>

<p>After creating the Docker file, I transferred all files to my GitHub profile.</p>

<br> </br>

<h2>Creation of virtual instances with AWS EC2.</h2>
<p>
For the creation of virtual instances, I used Amazon Web Service (AWS) and selected Amazon Elastic Compute Cloud (EC2) to create 4 instances that are eligible for the free tier. For creating virtual instances suitable for my application, I selected:
</p>
<ul>
<li><strong>Instance type</strong>: t2.micro</li>
<li><strong>Traffic authorization</strong>: HTTPS & HTTP (to configure an endpoint, for example, when creating a web server)</li>
<li><strong>Traffic module authorization</strong>: SSH (to connect to my virtual instance)</li>
<li><strong>Amazon Machine Image (AMI)</strong>: Ubuntu Server 22.04 LTS (HVM).</li>
<li><strong>Creating a key pair</strong>: for logging in using pem format for use with OpenSSH.</li>
</ul>

<p>After creating these 4 instances, I had to add additional security rules in addition to the default ones.</p>

<table>
<tr>
<th>PROTOCOL</th>
<th>PORT RANGE</th>
<th>SOURCE</th>
<th>DESCRIPTION</th>
</tr>
<tr>
<td>TCP</td>
<td>2376</td>
<td>0.0.0.0/0</td>
<td>Necessary for Docker Machine operations. Docker Machine is used to orchestrate Docker hosts.</td>
</tr>
<tr>
<td>TCP</td>
<td>2377</td>
<td>0.0.0.0/0</td>
<td>Used for communication between nodes of a Docker swarm or cluster.</td>
</tr>
<tr>
<td>TCP</td>
<td>7946</td>
<td>0.0.0.0/0</td>
<td>Used for node communication (container network discovery).</td>
</tr>
<tr>
<td>TCP</td>
<td>8501</td>
<td>0.0.0.0/0</td>
<td>Used as the default port for Streamlit applications.</td>
</tr>
<tr>
<td>UDP</td>
<td>4789</td>
<td>0.0.0.0/0</td>
<td>Used for overlay network traffic (inbound container network).</td>
</tr>
</table>

<p>To better organize these instances, I assigned them names:</p>
<ul>
<li>Node_Master</li>
<li>Node_1</li>
<li>Node_2</li>
<li>Node_3</li>
</ul>
<p>This is to make better use of Docker Swarm.</p>
<br></br>

<h2>Creation of a Docker Swarm consisting of one manager and three worker nodes.</h2>
<p>
To assign roles to the instances, I use Docker Swarm to create a Docker swarm consisting of one manager and 3 workers.
</p>
<p>
I start with booting up the Node_Master and enter these commands in the terminal:
</p>

<p> I update the list of available packages and their versions, but do not install or upgrade any packages. sudo allows running the command as a superuser (root), ensuring the necessary permissions to update the package lists. </p> 
<p> apt is the package manager used in Debian and Ubuntu distributions.</p>
<pre><code>
sudo apt update
</code></pre>
<p> I install Docker from your operating system's official package repository. Here again, sudo allows executing the command with root privileges, which are necessary to install software on the system. </p>
<p> docker.io is the package name for Docker in the official package repositories of Ubuntu and other Debian-based distributions. </p>
<pre><code>
sudo apt install docker.io
</code></pre>
<p> I start the Docker service using systemctl, which is a service management system for Linux that uses systemd. This command causes Docker (the background program) to start, allowing Docker containers to run on the system. Again, sudo is needed to obtain the appropriate permissions to start system services. </p>
<pre><code>
sudo systemctl start docker
</code></pre>
<p> I enable the Docker service to start automatically at system boot. This ensures that Docker is available even after a system reboot, without the need to manually start it each time. systemctl with enable creates the necessary symbolic links to start the Docker service during the system boot process. </p>
<pre><code>
sudo systemctl enable docker
</code></pre>
<p> I add the current user to the docker group, thereby allowing the user to execute Docker commands without needing to use sudo every time. </p>
<p> -aG stands for "append to group", and docker is the group name. ${USER} is an environment variable representing the current user's name.  </p>
<pre><code>
sudo usermod -aG docker ${USER}
</code></pre>
<p>
To verify that the changes were successful, I log out and log back into the following instance.
</p>
<p>
I proceed with assigning the manager role with this code:
</p>
<pre><code>
docker swarm init --advertise-addr 172.31.92.118
</code></pre>
<p>
obtaining output confirmation that this instance is now a manager and providing me with a code to assign the other instances the role of worker.
</p>
<pre><code>
docker swarm join --token SWMTKN-1-2ca4tuegeusncn42i02l8lw4yc8t8vzpj5ovw1ewm8i98h6tmp-eqouyv9esuom2moygvjgrltj8 172.31.92.118:2377
</code></pre>
<p>
I must enter this code into each worker instance I created to form a swarm.
</p>
<p>
I return to the manager node and use the following command to view all nodes with their respective roles:
</p>
<pre><code>
docker node ls
</code></pre>

<br></br>

<h2>Deployment of the application.</h2>
<p>
Before creating a service in the swarm, I decided to deploy the application through a particular method, namely:
</p>

<p> I clone the source code of a Streamlit application that has been prepared to run as a Docker container from my GitHub repository. </p>
<pre><code>
git clone https://github.com/Imkun-on/Streamlit-app-Docker.git
</code></pre>
<p> I list the files and directories in the current path, also to verify that the cloning was successful and to view the contents of the current working directory. </p>
<pre><code>
ls
</code></pre>
<p> I change the current directory to the newly cloned Streamlit-app-Docker directory, which contains the Dockerfile and the application source files. </p>
<pre><code>
cd Streamlit-app-Docker/
</code></pre>
<p> Again, I list the files and directories in the current directory, now inside Streamlit-app-Docker, to show the content of the application directory. </p>
<pre><code>
ls
</code></pre>
<p> I create a Docker image for the Streamlit application, using the Dockerfile in the current directory. The image is tagged with the name. </p> 
<pre><code>
docker build -t imkun/app-name-streamlit .
</code></pre>
<p> I list all the Docker images available on the system, allowing me to see the newly created image and any other images that might be present. </p>
<pre><code>
docker images -a
</code></pre>
<p> I start a Docker container in "detached" mode (in the background) using the imkun/app-name-streamlit image, mapping the container's port 8501 to the host's port 8501. </p>
<p> This allows me to access the Streamlit application via the browser at the host's address on port 8501. </p>
<pre><code>
docker run -d -p 8501:8501 imkun/app-name-streamlit
</code></pre>
<p> I list all the Docker containers currently running, allowing me to verify that the application container has started correctly. </p>
<pre><code>
docker ps
</code></pre>
<p> I stop a running Docker container, specifying the container's ID or name as an argument. </p>
<pre><code>
docker stop <container_name or id>
</code></pre>
<p> I remove all stopped Docker containers, cleaning the system from containers that are no longer needed. docker ps -a -q lists the IDs of all containers, and docker rm removes them. </p>
<pre><code>
docker rm $(docker ps -a -q)
</code></pre>

<br></br>

<h2>Creation of Services.</h2>
<p>
I create a Docker service in the context of a Docker Swarm cluster from the manager node, launching the application as a distributed service with 4 replicas (instances) of the container, making the application highly available and scalable.
</p>
<pre><code>
docker service create --name app-name-streamlit --replicas 3 -p 8501:8501 imkun/app-name-streamlit:latest (to be inserted into the code above)
</code></pre>
<p>I apply the same procedure for Postgres, Apache, and Redis services, specifying the number of replicas and service version (to see the service version, I went to Docker Hub): </p>
<pre><code>
docker service create --name redis --replicas 4 redis:latest
</code></pre>
<pre><code>
docker service create --name apache --replicas 4 httpd
</code></pre>
<pre><code>
docker service create --name postgres --replicas 1 \
  -e POSTGRES_PASSWORD=Databas3 \
  postgres
</code></pre>
<p>The reason I selected these services is because:</p>
<ul>
  <li><strong>Apache</strong>: can act as a reverse proxy, directing web requests to my Streamlit application. This allows me to securely expose your app to the Internet and better manage incoming traffic.
Moreover, if the application grows in popularity, Apache can help distribute the load among multiple application instances, improving performance and availability.</li>
  <li><strong>Redis</strong>: for asynchronous or long-duration operations, such as importing large data sets or performing complex analyses, Redis can manage job queues, improving the efficiency of the application.</li>
  <li><strong>PostgreSQL</strong>: can serve as the main database to store Yu-Gi-Oh! data, including decks, cards, game statistics, and more.</li>
</ul>
<p>
After creating these services, I check if they are all present: </p>
<pre><code>
docker service ls
</code></pre>
<p>Then I select any instance that is part of the swarm, connect, copy the public IP address, paste it into the browser, and enter port number 8501, and there you go, my app is visible. </p>

<br></br>

<h2> Creation of a Docker Stack so that no stack runs on the Manager node.</h2>
<p> Since we have many services, I use Docker Stack which allows me to deploy and logically group multiple services, which are containers distributed in a swarm. Therefore, I remove all the services I created.</p>
<pre><code>
docker service rm $(docker service ls -q)
</code></pre>
<p> Then I create a file with a yml extension specifying all the services I need to use in my streamlit and distribute the stack using this command:</p>
<pre><code>
docker stack deploy --compose-file docker-compose.yml my_stack
</code></pre>
<p> Finally, I look at both the services in my stack and also if they are not running on the management node through the following codes: </p>
<pre><code>
docker stack ls
</code></pre>
<pre><code>
docker stack ps my_stack
</code></pre>
<p> </p>
<br></br>


<h2>Storing the Docker Image on Docker Hub.</h2>
<p>
Before proceeding with the next command, I created a profile on Docker Hub to store the app.
</p>
<p> I log in to Docker Hub, allowing me to upload (push) or download (pull) Docker images. </p>
<pre><code>
docker login
</code></pre>
<p> I upload the “latest” tagged image of the application to Docker Hub under the name imkun/app-name-streamlit. </p>
<pre><code>
docker push imkun/app-name-streamlit:latest
</code></pre>
<p> I remove the specified Docker image from the local system. </p>
<pre><code>
docker rmi imkun/app-name-streamlit:latest
</code></pre>
<p> I download the Docker image imkun/app-name-streamlit from Docker Hub. </p>
<pre><code>
docker pull imkun/app-name-streamlit
</code></pre>
<p> As I did previously, I start a Docker container in the background using the specified image and mapping ports as indicated. </p>
<pre><code>
docker run -d -p 8501:8501 imkun/app-name-streamlit
</code></pre>


<h2> NOTE </h2> 
<p> Since the Streamlit app is missing some analyses to add and in case I decide to make changes, before proceeding with the deployment, I test the changes locally to ensure the application functions as expected. </p>
<p>I do this by running the Streamlit application locally </p>
<pre><code>
streamlit run app.py
</code></pre>

<p>After confirming that the changes work as expected, I go on to update the Docker image. </p> 
<p>This implies creating a new Docker image that incorporates the changes made.</p> 
<p>I use the Dockerfile to build the image, exactly as I did previously: </p>
<pre><code>
docker build -t username/app-name-streamlit:latest .
</code></pre>
<p> Once the updated image is created, I upload it to Docker Hub to make it accessible to the Docker Swarm nodes </p>
<pre><code>
docker push username/app-name-streamlit:latest
</code></pre>
<p>Finally, I tell Docker Swarm to use the updated image for the service running the Streamlit application. </p>
<p>If the service is already running, I can update it to use the new image with the command </p>
<pre><code>
docker service update --image username/app-name-streamlit:latest service-name
</code></pre>

<h2> NOTE</h2>
<p>If you are interested in exploring the data analysis I have conducted, I invite you to visit my site. Unlike this project, I did not use Streamlit for the analysis. You can find the site at the following address: <a href="https://www.kaggle.com/code/nezarec/eda-yu-gi-oh-cards" target="_blank">Yu-Gi-Oh Data Analysis on Kaggle 📊</a></p>

</body>
</html>
