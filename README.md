# SABDA

**Video Demo**: [Watch on YouTube](https://youtu.be/S1t3s2EGOq4?si=kF0vy8eoj9J1PyW8)

## Description

**SABDA** is a word guessing game where you try to guess a particular word that matches the description given below. To make it fun, the word is presented to you in a jumbled order, and using the letters + hint, you have to answer your guess within a given time frame.

It starts out slow with common words but can become quite difficult, especially if you pick the harder difficulties. You can also login to save your high score and rank in the leaderboards. Despite being a simple guessing game, there's a lot at stake which makes it even more fun.

> The maximum score you can currently get is by answering all 5 questions in the "God-Mode" difficulty level: **1000** points.  
> In the future, a continuous game mode that keeps going sounds fun too, but right now the game offers a set of 5 questions for each difficulty level which are re-generated every time.

---

## Project Files

Following typical protocol, the project folder `final_project2` consists of:

- `static/` — contains the CSS file  
- `templates/` — contains all HTML files  
- `app.py` — handles the rendering of webpages, loading of words, checking of answers, and almost everything  
- `final.db` — local SQLite database

---

## How Words Work

> I feel like the code could have been a lot cleaner had I known what I was doing!  
> But regardless, I learnt quite a number of things while trying to solve problems in this project.

One easy way to make it tighter is to use a single API capable of meeting requirements instead of gluing together three like I have done here.

### Here's how things work:

- **API 1** picks a random word based on length and language.  
- **API 2** is used to find the frequency of the word (how common it is).  
- **API 3** is used to find its meaning.  

Since I don't have access to paid APIs, this is the best I could conjure up. It takes longer because the second API might not have data for the word picked by the first API, and the third API may not have the definitions for the word validated before.

Doing this allows me to customise difficulty for the game by picking words of different length and frequencies.

---

## Game Modes

There are three game modes:

- **Easy**  
- **Try-Hard**  
- **God-Tier**  

The words in these modes are influenced by length and frequency in the English language.

The game has potential to add a "Marathon" or continuous mode in the future, with additional hints like:
- *Synonyms*
- *“The word begins with the letter x”*

But for now, the Try-Hard and God-Tier modes are a lot of fun. The Easy mode is there to help you get the game.

---

## Hurdles

### Route 1

> Well, it was NOT a smooth ride.  
> But keeping the occasional bugs aside, the major problem I faced was an architectural one.

It was *how* I picked and sent the words.

I naively thought picking a random word and sending that to the player was a good idea. But just one game played with this mode was enough for me to start from scratch. This 'architecture' was a bad idea for user experience — it could take 2 secs for your word to load or 10s — it wasn't consistent.

### Route 2

The second route I took showed some promise.

I would pick the whole set of words when the user chose a difficulty. This took some time (~30 sec), but once the game had loaded you could have a smooth playing experience.  
I even went as far as to suggest the user browse other sites and leave it in the background and played a sound when the game had loaded.

But ultimately, it didn’t feel polished enough.  
Sure, you could play if you waited 30 seconds — but what if you got the first question wrong? Would you honestly wait 30 seconds again to play the next time?

I felt it wasn't up to the mark.

### Route 3

After a bit of digging around, I found you could do something called **threading** in Python where you execute multiple things at once.

It was perfect for returning new questions to the server while doing stuff in the background.

I implemented the concept of a **cache**, where a set of questions for each difficulty level would be picked every time the server starts.  
This does mean it takes ~40–50s for the server to begin, but it's not something a user would notice. When the page loads and the user picks a difficulty, the words are already there.  

While this happens on the front, a new cache for that difficulty is being made.

This greatly improved the **user experience**, while costing a little bit on the processing side.

---

## Fun Things

### JSON

Getting acquainted with the **fetch API** and **JSON** was a plus.  
This project helped me understand how things were sent and how confirmations happened.

---

## License

This project was completed as a final project for [CS50X](https://cs50.harvard.edu/x/2025/).  
License terms follow the guidelines of CS50 projects. No commercial use is intended.

---
