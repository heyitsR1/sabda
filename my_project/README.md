#SABDA
#### Video Demo:  <https://youtu.be/S1t3s2EGOq4?si=kF0vy8eoj9J1PyW8>
#### Description:

SABDA is a word guessing game where you try to guess a particular word that mataches the description given below. To make it fun, the word is presented to you in a jumbled order, and using the letters + hint , you have answer your guess within a given time frame.

It starts out slow with common words but can become quite difficult, especially if you pick the harder difficulties.
You can also login to save your high score and rank in the leaderboards.
Despite being a simple guessing game, there's a lot of stake which makes it even more fun.

The maximum score you can currently get is by answering all 5 questions in the "God-Mode" difficulty level is 1000.
In the future, a continuous game mode that keeps going sounds fun too, but right now the game offers a set of 5 questions for each difficulty level which are re-generated everytime.

#### The Project Files:
Following typical protocol, the project folder "final_project2" consists of a "static" folder containing the css file and templates folder contains all HTML files, app.py and final.db are there as well. The app.py handles the rendering of webpages, loading of words, checking of answers, and almost everything.

#### How words work:
I feel like the code could have been a lot cleaner had I known what I was doing! But regardless, I learnt quite a number of things while trying to solve problems in this project. One easy way to make it tighter is to use a single API capable of meeting requirements instead of gluing together three like I have done here. Here's how things work: The first API picks a random word based on length, and language, the second API is used to find frequency of the word (or how common it is ) and the third one is used to find its meaning. Since i don't have access to paid APIs, this is the best I could conjour up, it takes longer because the second API might have data for the word picked by the first API and the third API may not have the definitions for the word validated before. Doing this allows me to customise difficulty for the game by picking words of different length and frequencies.

#### Game Modes:
There are three games modes: Easy, Try-Hard, God-Tier. The words in these modes are influenced by length and frequency in the English language. The game has potential to add a "Marathon" mode or 'continuous' mode in the future with additional hints like 'synonyms' or 'the word begins with the letter x'. But for now, the Try-Hard and God-Tier modes are a lot of fun. The 'Easy' mode is there to help you get the game.

### Hurdles:
#### Route 1
Well, it was NOT a smooth ride. But keeping the occassional bugs aside, the major problem I faced was an architectural one. It was "how" I picked and sent the words. For starters, I naively thought picking a random word and sending that to the player was a good idea. But just one game played with this mode was enough for me to start from scratch, this 'architecture' was a bad idea for user experience, it could take 2 secs for your word to load or 10s, it wasn't consistent.

#### Route 2
The second route I took showed some promise, I would pick the whole set of words when the user chose a difficulty. This took some time ~30sec but once the game had loaded you could have a smooth playing experience, I even went as far as to suggest the user to browse other sites and leave it in the background and played a sound when the game had loaded. But ultimately, it didn't feel polished enough. Yea, sure you could play if you waited 30 seconds, but what if you got the first question wrong...would you honestly wait 30 seconds again to play the next time? I felt it wasn't up to the mark.

#### Route 3
After a bit of digging around, I found you could do something called "thredding" in python where you execute multiple things at once. It was perfect for returning new question to the server as well as doing stuff on the background. I implemented the concept of 'cache' where a set of questions for each difficulty level would be picked everytime the server starts. This does mean, it takes ~40-50 s for the server to begin but it's not something a user would notice. But when the page would load, and the user would pick a difficulty, the words are already there. While this happens on the front, a new cache for that difficulty is being made. This greatly improved the User experience while costing a little bit on the processing side.


### Fun Things

#### JSON
Getting acquainted with the fetch API and JSON was a plus. This project helped me understand how things were sent and how confirmations happened.


