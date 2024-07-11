# Navigating the Linux Command Line
>**Edited by: Phumthep Bunnak**

If you are reading this tutorial, then more than likely you'll soon be using powerful computer clusters to run experiments. Many clusters operate on the Linux operating system, and in this tutorial, we'll cover the basics you need to know to get started.

### Understanding Linux and Its Importance
Linux distributions, often referred to as GNU/Linux to emphasize the complete operating system, have become increasingly popular due to their stability, security, and flexibility. The GNU component, pronounced "guh-new," is a recursive acronym for "GNU's Not Unix!" It is a free software project launched in 1983 by Richard Stallman with the goal of creating a complete Unix-like operating system composed entirely of free software[^1]. 

Building upon this foundation, Linux distributions, often called "distros," are complete operating systems that incorporate the Linux kernel, the GNU components, and other software packages like a text editor or a web browser. Each distro offers a unique user experience, differing in areas such as user interface design, software choices, and package management systems. Popular distros like Ubuntu, Mint, Fedora, and CentOS cater to various needs and preferences, providing users with options tailored to their specific requirements[^2].

Having explored the components of a GNU/Linux system, let's now turn our attention to how we interact with it. A shell acts as a bridge between you and the operating system, enabling you to issue commands and manage tasks. There are two main types of shells:
- Command-Line Interface (CLI) Shells: These offer a text-based interface where you type commands to perform actions. Bash and sh, mentioned earlier, are examples of CLI shells, interpreting your commands and executing them within the system.
- Graphical User Interface (GUI) Shells: GUIs provide a visual interface with familiar elements like windows, icons, and menus, offering a more user-friendly experience for those new to Linux.

While GUIs are available on Linux, mastering the CLI is essential for efficient cluster management. Command-line tools often streamline tasks, enable automation through scripting, and provide a reliable interface for remote access to the cluster, which is the primary mode of interaction in many research environments.

### Essential Commands for File System Navigation
Here are some fundamental commands you'll frequently use
- `pwd`: Prints the current working directory (where you are in the file system).
- `ls`: Lists files and directories in the current directory.
- `cd`: Changes the current directory.
    - Example: `cd project1` moves you to the project1 directory.
- `mkdir`: Creates a new directory.
    - Example: `mkdir data` creates a directory named data.
- `cp`: Copies files or directories.
    - Example: `cp report.txt ..` copies report.txt to the parent directory.
- `mv`: Moves or renames files or directories.
    - Example: `mv data_old data_new` renames the data_old directory to data_new.
- `rm`: Removes (deletes) files or directories.
    - Example: `rm file.txt` deletes file.txt. (Use with caution!)

For a more extensive list of commands, we can check out this [cheat sheet from DataCamp](#Bash & zsh Shell Terminal Basics Cheat Sheet | DataCamp)

### What's Next
In our next tutorial, we'll delve into using the command line to submit and manage your experiments on the cluster, covering job submission, resource allocation, and monitoring the progress of your computations.

But for now, try logging into a computer cluster and practice these basic commands to familiarize yourself with the command line environment. You’ll look just like a hacker in all those cool movies.

### Links
[^1]: Richard Stallman, the founder of the GNU Project, argues for the term GNU/Linux to emphasize that Linux is just one component of the operating system, and that the GNU Project provides many of the other essential components, such as compilers, libraries, shells, and utilities. See the GNU Project's website for more details: https://www.gnu.org/gnu/linux-and-gnu.html

[^2]: DistroWatch provides a comprehensive list and overview of Linux distributions: https://distrowatch.com/
