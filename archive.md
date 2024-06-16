# Archive

## Table of Contents

- [Archive](#archive)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Performance](#performance)
  - [Old Architecture (a big farewell for the last 2 years)](#old-architecture-a-big-farewell-for-the-last-2-years)
    - [Gitlab + Runner + Database (itbt 1)](#gitlab--runner--database-itbt-1)
    - [The Actual Prod Server (itbt 2)](#the-actual-prod-server-itbt-2)
    - [Backup (itbt 3)](#backup-itbt-3)
    - [Internet](#internet)
    - [DMZ (itbt 0)](#dmz-itbt-0)
  - [New Architecture (Hopefully it works)](#new-architecture-hopefully-it-works)

## Description

This File is a Dump of old information that was in the README.md file. This information is now outdated and is only kept for archival purposes.

## Performance

## Old Architecture (a big farewell for the last 2 years)

### Gitlab + Runner + Database (itbt 1)

We are chilling on:
- 8 Core/16 Thread Xeon
- 64GB RAM
- 1TB Storage

### The Actual Prod Server (itbt 2)

- 8 Core i7 (I think)
- 32GB RAM
- 500GB Storage

### Backup (itbt 3)

- Another 8 Core i7 (I think)
- 32GB RAM
- 250GB Storage

### Internet

- 1000mbps Glass Fiber from Deutsche Glasfaser

### DMZ (itbt 0)

- This was a Mac Mini, yes, just a Mac Mini with a djillion requests (yes, itbt 1 also is a reverse proxy; don't judge, no DMZ is perfect)

## New Architecture (Hopefully it works)

### All-In-One (itbt 1)

- 16 Core/32 Thread Xeon
- 64GB RAM
- 2TB SSD Storage
- 10TB HDD Storage
- 1000mbps Glass Fiber from Deutsche Glasfaser
- finally a DMZ that is not a Mac Mini
- hopefully a working reverse proxy
- hopefully a working database
- hopefully a working runner
- hopefully a working prod server
- hopefully a working backup server
- hopefully a working internet connection
- hopefully a working everything

> If you somehow manage to overload the new Server, then we will send you a happy letter containing an invitation to a public beating + the electricity bill.

> The Old Architecture was a bit overkill, but we had to use it because we had no other server. Now we have a server that is actually meant for this kind of stuff, so please don't overload it.
