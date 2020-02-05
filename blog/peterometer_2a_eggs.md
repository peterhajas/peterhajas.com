Title: Peterometer Chapter 2: Counting Raw Eggs
Date: 20200129 21:24
Emoji: 📊🥚

*This is the second in the Peterometer series. The first can be found [here](/blog/peterometer_1_hydration.html).*

After I felt comfortable tracking hydration, I wanted to introduce other metrics tracking into my life. I've been tracking the food I've eaten since March 2019. With less than a week of downtime, I've tracked **everything I've eaten** since that time.

I track my food in the [LoseIt](https://loseit.com/) app. I usually log the food right after eating it, and I really enjoy seeing how many calories I've eaten that day.

In the past year, I've also become *really* into eating raw eggs. I enjoy them on starchy foods, like ramen or rice. Kind of like my own version of [tamago kake gohan](https://en.wikipedia.org/wiki/Tamago_kake_gohan). In a given week, I'll end up eating a few meals with raw eggs.

But how many raw eggs? Let's find out!

# Exporting LoseIt Data

LoseIt lets you export the food you've eaten on a weekly basis from their website. These export as a CSV file, which is perfect for processing and backup. If you're a Premium member, go to your "Insights" tab on the website and then look for "Weekly Summary" and "Export to spreadsheet". I export my data every 2 or 3 weeks, and collect it all in a folder on my machine. These files are numbered based on their starting day since January 1 2000:

    $ ls
    WeeklySummary6637.csv
    WeeklySummary6644.csv
    WeeklySummary6651.csv
    WeeklySummary6658.csv
    WeeklySummary6665.csv
    WeeklySummary6672.csv
    WeeklySummary6679.csv
    ...

# Generating a master food CSV

I wrote a simple shell script to combine all these summaries, remove workouts (I track these separately), and then generate a master `combine.csv` file with all my food in one place:

    #!/bin/sh
    # delete the combine file
    rm combine.csv
    # concatenate all the csvs, sorting
    echo "Date,Name,Type,Quantity,Units,Calories,Fat (g),Protein (g),Carbohydrates (g),Saturated Fat (g),Sugars (g),Fiber (g),Cholesterol (mg),Sodium (mg)" > combine.csv
    cat *.csv | grep -v "Calorie Burn" | grep -v "Date,Name" | grep -v "HealthKit" | sort >> combine.csv

With this, we can `cat` out the combined CSV file to see the food I've eaten:


    $ cat combine.csv
    Date,Name,Type,Quantity,Units,Calories,Fat (g),Protein (g),Carbohydrates (g),Saturated Fat (g),Sugars (g),Fiber (g),Cholesterol (mg),Sodium (mg)
    01/01/2020,"Sandwich, Sub, JJ Gargantuan",Lunch,1.5,Each,"1,656",82.50,108,124.50,22.50,n/a,7.50,268.50,5121
    01/01/2020,Cookie,Snacks,4.0,Servings,144,12,4,72,6,32,0,0,230
    ...

(this example highlights a problem with my use of `sort` in the script: 01/01/2020 sorts alphabetically before 12/01/2019)

# Analyzing the food I've eaten

We can use some simple utilities to query the file. For example, how many food entries have I logged?

    $ cat combine.csv | wc -l
    3984

Wow! That's a lot of food. This averages to around 12 entries per day.

We can `grep` for other data, like how many burritos I've had.

    $ cat combine.csv | grep -i burrito | wc -l
    38

I've eaten a burrito every 9 days or so.

# Counting raw eggs

But **how many raw eggs** have I eaten? I usually log these when I eat *actual raw eggs* (when I cook an egg dish on the stove without oil I will also count it as raw eggs). Let's `grep` the CSV file:

    $ cat combine.csv |grep -i egg
    01/02/2020,Egg raw,Dinner,2.0,Servings,140,9.60,12.60,0.80,3.20,n/a,n/a,372,142
    01/02/2020,Scrambled Eggs,Breakfast,1.0,Each,91,7,6,1,2,0.80,0,169,88
    ...

This `grep` picked up anything with "egg" in the title, like scrambled eggs. We only want to look for raw eggs - it's simple enough to do that by modifying our `grep` invocation. But keep in mind the header line of `combine.csv`:

    Date,Name,Type,Quantity,...

The fourth column is the *quantity*. This is how many raw eggs I actually ate. So we really want to sum that column.

We can print the fourth column with a bit of `awk`:

    $ cat combine.csv |grep -i egg |grep -i raw | awk -F, '{ print $4; }'
    2.0
    2.0
    2.0
    2.0
    2.0
    ...

and sum it with a bit more:

    $ cat combine.csv |grep -i egg |grep -i raw | awk -F, '{ eggs+=$4; } END { print eggs; } '
    276.75

(yes, I did eat non-whole portions of eggs some days)

276.75 raw eggs. That's nearly two dozen dozen raw eggs!

# Raw egg consumption based on day of the week

As a fun visualization, I wanted to see if I ate raw eggs more on a particular day of the week. I did this using some simple categorization in Numbers:

![Raw eggs visualized by day](/media/peterometer_2a_eggs_per_day.png)

Wow! Based on this, I had way fewer raw eggs on Fridays. Tuesdays and Thursdays are lighter weekdays for raw egg consumption.

# Looking forward to more food analysis

Counting raw egg was a fun test of the data I've been gathering for the past 10 months. I'm really excited about the other visualizations and analysis I can do on the food that I've eaten.

