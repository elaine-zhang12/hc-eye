console.log('Script is connected!');

let reading_passages = [];
let current_index = 0;

async function fetchPassages() {
    try {
        const response = await fetch('./passages.json');
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        reading_passages = await response.json();
        console.log('reading_passages', reading_passages); // JSON data as a JavaScript object

        // Return the first passage initially
        return reading_passages[current_index]["text"];
    } catch (error) {
        console.error('Error fetching the JSON file:', error);
    }
}

function displayPassage(passageText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(passageText, 'text/html');
    const paragraphs = doc.querySelectorAll('p');
    const text_passage_display = document.getElementById('textPassage');
    text_passage_display.innerHTML = '';

    paragraphs.forEach(p => {
        const newParagraph = document.createElement('p');
        newParagraph.textContent = p.textContent;
        text_passage_display.appendChild(newParagraph);
    });
}

function changePassage(index) {
    current_index = parseInt(index, 10); // Convert index from string to number
    const selectedPassage = reading_passages[current_index]["text"];
    displayPassage(selectedPassage);
}

async function fetchFontSize() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_font_size');
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        font_size_response = await response.json();
        console.log(font_size_response)

        // Return the first passage initially
        return font_size_response["font_size"];
    } catch (error) {
        console.error('Error fetching the font size:', error);
    }
}

    const textBox = document.getElementById('textBox'); // Get the text box element
    const backspaceCountDisplay = document.getElementById('backspaceCount'); // Get the backspace count display
    let backspaceCount = 0; // Initialize backspace count

    // Listen for keydown events on the text box
    textBox.addEventListener('keydown', (event) => {
        if (event.key === 'Backspace') {
            backspaceCount++; // Increment backspace count
            backspaceCountDisplay.textContent = `Backspace count: ${backspaceCount}`; // Update display
        }
    });
    console.log("Backspace count: " + backspaceCount)


async function main() {
    // Fetch and display the first passage initially
    const firstPassage = await fetchPassages();
    if (firstPassage) {
        displayPassage(firstPassage);
    }
    const text_passage_display = document.getElementById('textPassage'); // Get the element
    setInterval(async () => {
        const font_size = await fetchFontSize(); // Function to fetch the font size

        text_passage_display.style.fontSize = font_size + 'px'; // Update the font size
    }, 5000); // Execute the code every 5000ms (5 seconds)
    
}

main();
