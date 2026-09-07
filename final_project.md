# BSD Release Monitor

## For Whom / Why?
It allows people to find information on all BSD Operating Systems without the need to visit loads of websites, which can take a while to look through. My website has a table that contains – Name, Package Manager, CPU Architecture, Latest Version, and End of Support (for the latest version). An example of a use case is that someone might be interested in a system but not too sure if it supports their CPU architecture – they can look on the website, see a list of operating systems, and choose the one that is supported on their system. It saves hours of research.

## 2-4 Planned Models
1) Comment – Stores user, comment text, date, and which BSD it belongs to. DONE
2) User – Stores usernames and passwords so comments are attributed to someone. DONE

## 3-5 Features
1) Edit / delete rows – This will allow the user to update the data when there is a new release of the BSD system.
2) Search – Type in a name of the distribution to display information based on it. For example, if the user types "GhostBSD", it only displays information for GhostBSD.
3) Comment – People will be able to add their own comments to each distribution. DONE ALL THAT

## What's Already Done in hw3
I created a BSD operating systems monitor with a data table showing Name, Package Manager, CPU Architecture, Latest Version, and End of Support. I also implemented an "Add BSD Operating System" form that appends a new row to the table. The mini-project directly connects to my final topic because the existing table becomes the main BSD list page, and the add form is one of the core features. For the final project, I will extend this by adding edit/delete functionality, search/filter, and user comments with authentication.
