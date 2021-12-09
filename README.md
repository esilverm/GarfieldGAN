# GarfieldGAN

## Introduction

For this project I wanted to create a GAN that could generate images of a cat. Not just any cat, however. I wanted to have it generate pictures of garfield. The GAN would be trained on panels from the Garfield comic strip and would then be reconstructed to show a brand new comic.

### Inspiration

[![Lasagna Cat](https://consequence.net/wp-content/uploads/2017/02/screen-shot-2017-02-09-at-12-41-20-pm.png?resize=198)](https://youtu.be/NAh9oLs67Cw)

In recent years, Garfield has underwent a period of ironic meme-ization. This is evidenced by youtube channels such as [Lasagna Cat](https://www.youtube.com/user/lasagnacat) created by Fatal Farm, and works such as [Garfield Minus Garfield](https://garfieldminusgarfield.net/) (or even [Garfield minus Jon](http://garfieldminusjon.thecomicseries.com/)).

![1/5/84 Garfield minus Garfield](https://64.media.tumblr.com/fSymsOGXOcec5jolC5qykwgo_500.gifv)

![5/12 Garfield minus Jon](https://img.comicfury.com/comics/3ec908306fc26bfcae5cf0b57323ade51930174392.png)

In the ML arts space, there have been several very interesting projects involving Garfield that are worth mentioning. YouTuber CodeParade [generated full comics with Neural Networks](https://www.youtube.com/watch?v=wXWKWyALxYM) by training entire 3 panel comics. Github user vdalv wrote a [GAN trained on solely images of Garfield](https://vdalv.github.io/2018/12/04/ganfield.html). A team of researchers explored [comic strip completion with GANs](https://medium.com/@neelansh5_9493/comic-strip-generation-794cb67bc79). The idea of bridging Garfield with AI has been in the air for some time, but has been explored in many different ways.

## Process

### Data Collection

The process to put this together consisted of several steps. First was data collection. For this I wrote a webscraper using Scrapy. It would visit [this Garfield Comic Database](http://pt.jikos.cz/garfield/) and collect all image URLs from a certain year through present day. The code can be found [here](/src/scraper/spider.py).

Since I wanted to train on ONLY three panel comics, I filtered out Sunday comics with the following line of code:

```python
if not datetime.datetime.strptime(
  comic.css("img::attr(alt)").get()[9:], "%d/%m/%Y").weekday() == 6
```

This essentially gets the alt-code of the image on the site (which should contain the date of the current comic) and converts it to a number representing which weekday it was posted on (6 being Sunday).

After this I needed to preprocess all the images. In the file [preprocess.py](/src/preprocess.py) I went through the jsonl file produced by scrapy and downloaded each image from the site. Since they were in gif format, I had to convert them to png or jpeg so they could be processed by the model I wanted to use. I also cut them in thirds by using Pillow, a python image manipulation library. Early iterations of my code included saving files that were mirrored horizontally. Because StyleGan takes care of this by default, I eventually removed these images from my training set.

### Training

For this project I wanted to attempt to use the most modern version of StyleGAN on NYU's Greene Supercomputer.

This version, [StyleGAN3](https://github.com/NVlabs/stylegan3/tree/a5a69f58294509598714d1e88c9646c3d7c6ec94), uses augmentations such as rotations, translations, and color changes to add new images to any dataset so even small datasets can be learned from.

Since I am relatively new to GANs I went in using default values and set out to train my model. Unfortunately I severely underestimated how long I would need to train this model as well as a few other key things. Here are a few things I didn't realize

- **I should've turned off augmentations outside of color changes.** Because I allowed this, things such as image borders appear as diagonal lines cutting through the image and look off
- **I need to allocate at least a week of training time to this.** I only allocated 4 days thinking it would be enough. I was wrong. It only made it halfway through training.
- **I probably should've done some kind of data cleaning before training**. Almost immediately after training started I realized a lot of the generated examples of my images were the same. This is due to a thing called _mode collapse_. Mode collapse is an issue where there are lots of repeated values and the generator learns that it can trick the discriminator into thinking things are real by producing only a variety of values that are close to the real thing but not it. (Here)[https://aiden.nibali.org/blog/2017-01-18-mode-collapse-gans/] is a good resource that helped me learn more about this issue and why my training had issues.

As of right now, my work on this isn't done. I still am working on training a model with StyleGAN2 to see if I can address mode collapse with an earlier form of StyleGAN.

### Looking to the future of this project

I am currently training a StyleGAN2-ada model with the same image set in an attempt to fix the issues I have addressed earlier. I have modified some of my settings that I used (previous StyleGAN3 ones can be found (here)[/src/run_training.slurm]) and preliminary tests seem to be working. For instance, I found that after 200kimgs I got pretty rudimentary images with slight variations that picked up stuff like speech bubbles. I am hoping that after a thorough training, that my model will be able to produce images like other models, but there is still a ways to go when it comes to perfecting this stuff.

Also I had hoped to be able to have a website where I could display these generated Garfield panels. This has not come to fruition, but it is on my todo list for the future!

## Preliminary results

### StyleGAN3

The last snapshot of training from StyleGAN3
![The final image of training when StyleGAN3 completed](https://i.imgur.com/q9txjbS.jpg)

### StyleGAN2-ada

200kimg of StyleGAN2-ada
![200kimg of stylegan2](https://i.imgur.com/YGaA2Ad.png)

Want to see more images? [Click Here](https://drive.google.com/drive/folders/1LpUxbSoj4OMT4HulJobUu3nBZDOFPADC?usp=sharing)
