Title: Declarative Home Automation
Date: 20220521 20:30

My home is powered by [Home Assistant](https://www.home-assistant.io), which is a great software package for running a smart home. In this post, I'll talk about how I'm automating my home *declaratively* rather than using an "if-this-then-that" approach.

# Lighting The Patio

We have lights on our patio. I want them on if:

- it's after sunset and before 9:00PM
*or*
- the patio door was opened within the last 3 minutes at night (if I'm going outside, or letting the dogs out)

## The Classic Model: "If-This-Then-That"

If you did an "if-this-then-that" approach, you might have rules like:

- if it's after sunset but before 9:00PM, turn the lights on
- if the back door opens while the sun is below the horizon, turn the lights on for 3 minutes

While these rules sound simple, they have edge cases that will bite you when the cases fight each other. Imagine I'm letting the dogs out at 8:59PM. Following the above rules:

1. Door opens at 8:59PM, and the lights turn on
2. 9:00PM comes, and the lights turn off
3. I'm out in the dark!

You could solve this by introducing more state. You might add a "lights on due to time" and "lights on due to door opening" state to bookkeep when to perform actions of the automation. But what if we add another rule? For example: if the back camera detects a person or dog, turn the lights on for three minutes.

Adding additional "what am I doing" state makes the complexity explode for state bookkeeping.

## A Declarative Model: "Should" [State](State.md)

In my smart home, I take all this input state and derive a "should be" state out of it. The patio light automation has just one rule:

- If the patio lights *should* be on, then turn them on. Otherwise turn them off.

I define these "should be" states with simple boolean logic in a [template binary sensor](https://www.home-assistant.io/integrations/template/). Here's the one for my patio lights:

    template:
      - binary_sensor:
        - name: "Patio Lights Should Be On"
          delay_off:
            minutes: 3
          state: >
            {% set before9 = now().hour < 21  %}
            {% set doorOpen = states('binary_sensor.patio_door') == 'on' %}
            {% set night = is_state('binary_sensor.night', 'on') %}
            {% set people = is_state('binary_sensor.patio_person_motion', 'on') %}
            {% set dog = is_state('binary_sensor.patio_dog_motion', 'on') %}
            {{ night and (before9 or doorOpen or people or dog) }}

I have a simple [blueprint](https://www.home-assistant.io/docs/automation/using_blueprints/), `binary_sensor_entity`, that manages these automations for me:

    blueprint:
      name: Binary Sensor to Entity
      description: Tie a binary sensor (likely from a template) to an entity state
      domain: automation
      input:
        source_sensor:
          name: Source Sensor
          description: This sensor will be used to drive the entity
          selector:
            entity:
              domain: binary_sensor
        target_entity:
          name: Target Entity
          description: The entity to be driven by the sensor
          selector:
            entity:

    variables:
      source_sensor: !input source_sensor

    trigger:
      - platform: state
        entity_id: !input source_sensor

    action:
      - service: >
          {% if is_state(source_sensor, "on") %}
            homeassistant.turn_on
          {% else %}
            homeassistant.turn_off
          {% endif %}
        entity_id: !input target_entity

This makes the patio lights automation very simple:

    automation:
    - alias: Lights - Patio - Primary
      use_blueprint:
        path: binary_sensor_entity.yaml
        input:
          source_sensor: binary_sensor.patio_lights_should_be_on
          target_entity: switch.patio_shelly_channel_1

My entire home is driven this way. I think this is easier to understand and extend than the classic way of doing Home Assistant automations. I also prefer it over [Node-RED](https://nodered.org), although I still use Node-RED for some tasks in my home (this may be a subject of a future post).

I like how well this addresses the edge case described above, and how easy it is to experiment with new states driving the "should be" sensors. I tried keeping the lights on during severe weather (I have since removed this), and it only took one change to the "should be" sensor for the patio lights. These sensors are also really easy to debug - you can view them in the History section of Home Assistant.

Please feel free to [drop me a line](/about.html) if you have any feedback on this post. Thanks for reading!

