We’ll start, as always, with an Nmap scan:

`nmap -sCV -n 10.10.11.68`

It shows two open ports: 22 and 80.  
![[../img/Planning_1.png]]

So, there's a web server running on port 80. After adding the domain to `/etc/hosts`, we can access the landing page.  
![[../img/Planning_2.png]]

You can explore the site a bit, but there doesn’t seem to be much going on here (at least from what I can tell).  
What I usually do at this point is look for hidden subdirectories like `/login`, and also check for subdomains.

To find subdirectories, I use **feroxbuster**:  
![[../img/Planning_3.png]]

As you can see, nothing interesting came up.  
However, when running Gobuster to search for subdomains, something suspicious appears:

`gobuster vhost -w /usr/share/seclists/Discovery/DNS/combined_subdomains.txt -u http://planning.htb --ad -t 500`

![[../img/Planning_4.png]]

We can see that it has a login page:

![[../img/Planning_5.png]]

After logging in with the provided credentials, the first thing we can check is the version that’s running:

![[../img/Planning_6.png]]

When we search for exploits for this version, we see that we can get RCE pretty easily if it's version 11.0.0.

![[../img/Planning_7.png]]

---

**Little tip if you're having issues with the PoC from nollium:**

When I tried this PoC → [https://github.com/nollium/CVE-2024-9264](https://github.com/nollium/CVE-2024-9264), I was able to run some commands, but couldn’t actually get a reverse shell.

To figure out why it failed, I compared it to the PoC from **z3k0sec**, whose version **does** give you a reverse shell.

If you look at both scripts, you'll notice the main difference is in how the commands are triggered. While _nollium_ injects the command into a file and immediately tries to execute it with `bash`, _z3k0sec_ writes the command into a file and then **triggers it separately** with another request.

You can see that here:

![[../img/Planning_8.png]]

And then compare it to the working one:

![[../img/Planning_9.png]]  
![[../img/Planning_10.png]]

**TL;DR:** If you want to use the first script, just change the query to:

![[../img/Planning_11.png]]

And it’ll work.

![[../img/Planning_12.png]]

---

Now we're inside. The first weird thing is that we're already root. Maybe the flag is in `/root/root.txt`?

Life’s not that easy 😅  
![[../img/Planning_13.png]]

I tried `sudo -l` but it doesn't work, so I’ll just run **LinPEAS** and see what shows up.

Here’s how to bring LinPEAS to the machine:

![[../img/Planning_14.png]]

We see something interesting in the environment variables — an admin username and a password:

![[../img/Planning_15.png]]

If we try to access SSH with that user, it lets us in and we can grab the `user.txt` flag:

![[../img/Planning_16.png]]

Again, `sudo -l` doesn’t work, so I’ll try LinPEAS again. When running it, I notice some crontabs running, and also that there’s a service on port 8000, but I’m not able to trigger it using `curl`.

![[../img/Planning_17.png]]

With this command, we can tunnel the remote port 8000 to our local port 80:

`sudo ssh -L 80:localhost:8000 enzo@planning.htb`

When we access `http://localhost`, we see a login page:

![[../img/Planning_18.png]]

Okay, so we need a password again. Looking back at the LinPEAS output, we see a file with a password that seems to be related to the crontabs:

![[../img/Planning_19.png]]

We can log in to the page using `root` as the user and the password found earlier — it’s the one used to encrypt backups.

Once inside, we can create a crontab. Since it runs as root, this is pretty straightforward.

![[../img/Planning_20.png]]

Click on **"Run Crontab"**, and we’ll get the flag.

To get a root shell, just add or edit the crontab and include something like this:

`cp /bin/bash /tmp/bash && chmod u+s /tmp/bash`

This copies the `bash` binary to `/tmp`, makes it executable by anyone as root (because of the SUID bit), and then you can run:

`/tmp/bash -p`

to pop a root shell.

![[../img/Planning_21.png]]