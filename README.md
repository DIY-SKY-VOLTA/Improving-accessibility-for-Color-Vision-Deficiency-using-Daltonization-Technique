#                                  Original Image
![0 Original Apples](https://github.com/user-attachments/assets/c648603b-d104-4203-b4fe-3f53d730b5a7)


#                            Daltonized (Recoloring) Images
![simulated-gif-maker](https://github.com/user-attachments/assets/5a08ef6c-c83e-46f2-b721-45d291a603bd)
Filters clonned from Daltonize.org, a chrome extension consists of Protanopia, deutanopia, Tritanopi, Enhance - R, Enhance - G
Credit: http://www.daltonize.org/

# Simulated Images
![Simulated-maker](https://github.com/user-attachments/assets/c0b798b0-7ea7-412b-a2d6-b6ad983d58a9)

# Understanding Color Vision Deficiency and Accessibility Technologies
For detailed information: Daltonize.org http://www.daltonize.org/


Color Vision Deficiency (CVD) is a visual impairment affecting the perception of colors. This document explains CVD, the concept of Daltonization, simulation techniques, and the application of object segmentation and color recognition in designing accessible solutions for CVD.

---

## What is Color Vision Deficiency (CVD)?
Color Vision Deficiency, commonly referred to as **color blindness**, is the inability to perceive colors accurately due to deficiencies in the cone cells of the retina. It affects millions of individuals worldwide and can be categorized into:

# Types of Color Vision Deficiency (CVD)

Color Vision Deficiency (CVD), commonly referred to as color blindness, affects the ability to perceive colors accurately. It can vary in severity and is typically classified into the following types:

## 1. **Red-Green Color Vision Deficiency**
This is the most common type of CVD and involves difficulty in distinguishing between red and green hues.

### a. **Protanomaly** 
- Reduced sensitivity to red light.
- Red colors may appear more muted or brownish.

### b. **Protanopia**
- Complete inability to perceive red light.
- Red may appear black, and certain shades of orange, green, and yellow can be indistinguishable.

### c. **Deuteranomaly**
- Reduced sensitivity to green light.
- Greens and yellows may appear similar.

### d. **Deuteranopia**
- Complete inability to perceive green light.
- Green and red hues may appear indistinguishable.

---

## 2. **Blue-Yellow Color Vision Deficiency**
This type is less common and involves difficulty distinguishing between blue and yellow shades.

### a. **Tritanomaly**
- Reduced sensitivity to blue light.
- Blue may appear greenish, and yellow can appear pale or indistinct.

### b. **Tritanopia**
- Complete inability to perceive blue light.
- Blue may appear green, and yellow may look pinkish or gray.

---

## 3. **Monochromacy (Total Color Blindness)**
This is a rare form of CVD where individuals perceive no color at all. It is subdivided into:

### a. **Cone Monochromacy**
- Only one type of cone cell functions, leading to a limited color spectrum.

### b. **Rod Monochromacy (Achromatopsia)**
- No functional cone cells.
- Vision is entirely grayscale, and light sensitivity is often increased.


CVD can impact daily activities, learning, and accessibility, making it essential to design tools and technologies that accommodate such individuals.

---

## What is Daltonization?
Daltonization is a computational technique that modifies images or visual content to enhance color differentiation for individuals with CVD. It works by:

1. **Adjusting Colors:** Modifying the hues and contrasts to make colors distinguishable for users with specific deficiencies.
2. **Replacing Confusing Colors:** Substituting indistinguishable colors with perceptually distinct ones.
3. **Enhancing Accessibility:** Ensuring that critical information (e.g., graphs, charts, and labels) is visible to all users.

Daltonization is widely used in:
- **Education:** Making charts and graphs more readable.
- **Healthcare:** Highlighting key elements in medical imaging.
- **User Interfaces:** Improving accessibility for digital platforms.

---

## What is Simulation?
**Color Vision Simulation** is the process of mimicking how individuals with different types of CVD perceive colors. It helps developers, designers, and educators understand how their content or designs appear to users with CVD.

### Applications of Simulation:
- **Testing Accessibility:** Evaluating whether designs are inclusive and easy to understand.
- **Creating Awareness:** Helping people without CVD empathize with those who experience it.
- **Improving Content:** Allowing for adjustments to improve usability and readability.

Popular tools like **Coblis** and **Color Oracle** provide real-time simulations for different types of color vision deficiencies.

---

## Object Segmentation and Color Recognition for CVD
**Object Segmentation** and **Color Recognition** are advanced techniques used to enhance accessibility for individuals with CVD:

### 1. **Object Segmentation**
- Involves identifying and isolating specific objects within an image or video.
- **How It Helps CVD Users:**
  - Segments important elements (e.g., graphs, text, diagrams) for focused enhancement.
  - Allows for the application of color correction (Daltonization) to selected areas.

### 2. **Color Recognition**
- Uses algorithms to detect colors and provide context or labels for CVD users.
- **How It Helps CVD Users:**
  - Labels colors with text (e.g., "This is red").
  - Converts confusing color regions into patterns or textures.
  - Assists in distinguishing between similar colors using overlays or augmented visuals.

### Technologies Involved:
- **AI and Machine Learning:** Enhancing the precision of object recognition and adaptation.
- **Computer Vision Tools:** Libraries like OpenCV for real-time video processing.
- **Augmented Reality:** Providing overlays to improve real-world color perception.

---

## Applications and Future Directions
The integration of Daltonization, simulation, object segmentation, and color recognition can revolutionize accessibility in various fields:
- **Education:** Real-time adaptation of educational materials for students with CVD.
- **Healthcare:** Enhancing medical visuals for practitioners with CVD.
- **Entertainment:** Adapting videos, games, and media to make them more inclusive.
- **Navigation:** Assisting CVD users in recognizing traffic signals or signage.

Our project aims to combine these technologies into an AI-powered solution to make visual content universally accessible.

---

## Contributing
We welcome contributions to improve this project, add new features, or refine existing techniques. Please open an issue or submit a pull request with your suggestions.

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

Inspired from Daltonize.org http://www.daltonize.org/
