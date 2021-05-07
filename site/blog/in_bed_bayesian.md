Title: Detecting Whether I'm in Bed or Not
Date: 20210506 18:15
Emoji: 🛌📊

# Some Background

I've been learning about and using [Home Assistant](https://www.home-assistant.io) for the past few months. It's an open source home automation platform, but it can be turned into much more. It's kind of like your own personal "if-this-happens, do-that" service.

At the core of the system are *entities*, which represent stuff the system knows about. Entities are prefixed with their *type*, for example `person.peter_hajas`, `light.bedside_table`, `sensor.patio_temperature`, or `sun.sun`. Home Assistant supports a suite of user-authored entities for sensors (things that feed the system data), commands (actions triggered by the system), and semantic devices (like "covers", Home Assistant's catchall for garage doors, sun shades, etc.).

# Building the Sensor

One of the platforms for a binary sensor (determines if something is true or false) is the [Bayesian](https://www.home-assistant.io/integrations/bayesian/) binary sensor. This lets you use [Bayes' theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem) to combine observations into a sensor value.

While spending some time at my home alone recently, I wanted to play with automations keyed off of whether or not I was in bed. This could be used to shut off lights and turn off appliances. I've read about some of the [bed occupancy sensors](https://everythingsmarthome.co.uk/howto/building-a-bed-occupancy-sensor-for-home-assistant/) you can build, but I wanted to see how far Bayesian sensing could get me.

Here's my "am I at home in bed" `binary_sensor`:

```
# Am I at home in bed?
- platform: bayesian
  name: "peter_in_bed"
  prior: 0.33
  probability_threshold: 0.9
  observations:
    - entity_id: "person.peter_hajas"
      prob_given_true: 0.5
      platform: "state"
      to_state: "home"
    - entity_id: "sensor.phajas_phone_battery_state"
      prob_given_true: 0.75
      prob_given_false: 0.05
      platform: "state"
      to_state: "Charging"
    - entity_id: "sun.sun"
      prob_given_true: 0.75
      platform: "state"
      to_state: "below_horizon"
    - entity_id: "binary_sensor.orion_active"
      prob_given_true: 0.4
      platform: "state"
      to_state: "off"
```

These sensors are written in YAML. You describe a prior (at any given time, how likely is it this is true?), an optional threshold (only be true if the chance is above the threshold), and observations. These observations are in terms of entities or Home Assistant templates. Here's a breakdown of this sensor:

- There's a 33% chance I'm in bed, represented by the `prior`. This assumes I spend 8 hours in bed.
- I only want the sensor to trigger when the sensor is at least 90% confident. It'd be annoying if it activated at a lower threshold. This is set in `probability_threshold`.
- If I'm at home, there's a 50% chance of me being asleep (this is a bit less true while working from home, but tracks for a typical commute schedule).
- If my phone is charging, there's a 75% chance I'm asleep. I usually only charge at night, so if I'm unplugged, there's only a 5% chance of me being in bed.
- If the sun is below the horizon, there's a 75% chance that I'm in bed.
- If my workstation (Orion) is not active, there's a 40% chance that I'm in bed.

# How Well Does it Work?

I'd say it works pretty well. Some observations:
- It's awesome to throw the phone on the nightstand charging pad and have everything shut off.
- It stinks when I charge my phone at night and everything turns off. I might need to play with the probabilities (if my machine is logged in, there's basically a 0% chance I'm in bed, for example) or add other sensing (did another room recently see motion?) to help in this case.
- I have yet to try it with multiple users :-). My wife (yes, wife! More on this in a future post) would need her own version of this sensor to enable turning lights off, otherwise I could leave her in the dark.
