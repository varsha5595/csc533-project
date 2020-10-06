## Analyzing Privacy Vulnerabilities of  Third-Party Skills in Alexa

Privacy Project for CSC 533

Smart speakers have been popularly used around the world, mainly due to the convenience brought from the virtual personal assistant (VPA) which offers interactive actions through the convenient voice commands from users. Besides the built-in capabilities, VPA services can be further extended by third-party developers through skills. These skills attract users together with malicious developers. We plan to implement a skill explorer to systematically explore the interaction behaviors of skills developed for Alexa and identify the ones which violate the users’ privacy. The skill explorer will analyze the Alexa skills listed on the Amazon marketplace.

## Setup

### Obtaining the privacy policy
1. Navigate to any skill on the Amazon market place
2. Under the "Skill details" section, click on "Privacy Policy"
3. A new tab opens in the browser displaying the privacy policy with an alpha-numeric Skill ID displayed in the URL. Save this page as an HTML document and name it as \<skillID\>.txt
 
### Converting the privacy policy to plaintext
The project uses an external system known as PolicyLint to convert a privacy policy of a skill from HTML to plain text:
1. Navigate to the [PolicyLint](https://github.com/benandow/HtmlToPlaintext) project
2. Follow the README to setup and execute the PolicyLint converter
3. From the root folder of the project, copy the "plaintext_policies" folder located at /ext/plaintext_policies

### Project setup
1. Clone this repository
2. Paste the "plaintext_policies" folder at the root level of the project

## Execution
```
cd src
python3 main.py
```
## Authors

* Shivaprakash Balasubramanian
* Varsha Anantha Ramu Sharma

## License

This project is licensed under MIT License
