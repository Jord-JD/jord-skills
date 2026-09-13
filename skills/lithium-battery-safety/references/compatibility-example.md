# Battery compatibility example

This is a worked example from the original skill, not a current compatibility certificate. Recheck the linked documents and exact product revisions before applying its conclusion.

## Example

Your user is a hobby electronics enthusiast and has a Waveshare ESP32-S3-Touch-LCD-2.8. They want to charge it with a Pi Hut PKCell 2000 mAh battery.

This might seem safe at first glance, but you must look up the datasheets, schematics, specifications, etc. for both the board and the battery online. In this case, you would find that the Waveshare ESP32-S3-Touch-LCD-2.8 uses an ETA6098 charger with an 82 kΩ charge-current resistor. The ETA6098 datasheet specifies that 82 kΩ configures the charger for approximately 2 A fast charging, with a 4.2 V constant-voltage phase. The Pi Hut PKCell 2000 mAh battery's datasheet specifies a maximum constant charging current of 1.5 A. Therefore, charging the Pi Hut PKCell 2000 mAh battery with the Waveshare ESP32-S3-Touch-LCD-2.8 would exceed the battery's maximum charging current and could be dangerous. Do not connect or adapt this battery for use with this board: the charging-current limit is already exceeded, and the connectors are not directly compatible.

Sources for this example:

* [Waveshare board resources and schematic information](https://docs.waveshare.com/ESP32-S3-Touch-LCD-2.8/Resources-And-Documents)
* [Waveshare ESP32-S3-Touch-LCD-2.8 schematic](https://files.waveshare.com/wiki/ESP32-S3-Touch-LCD-2.8/ESP32-S3-Touch-LCD-2.8-Schematics.pdf)
* [ETA6098 charger datasheet](https://www.eta-semi.com/wp-content/uploads/2022/03/ETA6098_V1.1.pdf)
* [Pi Hut PKCell 2000 mAh battery listing](https://thepihut.com/products/2000mah-3-7v-lipo-battery)
* [2019 PKCell LP803860 2000 mAh battery datasheet linked by Pi Hut](https://cdn.shopify.com/s/files/1/0176/3274/files/LP803860_2000mAh_3.7V_20190510.pdf?v=1665420199)
