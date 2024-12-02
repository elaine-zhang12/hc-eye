// console.log("Script is connected!");

// let reading_passages = []
// let current_passage = ""
// async function fetchPassages() {
//     try {
//     const response = await fetch('./passages.json');
//     if (!response.ok) {
//         throw new Error('Network response was not ok ' + response.statusText);
//     }
//     const reading_passages = await response.json();
//     console.log("reading_passage", reading_passages); // JSON data as a JavaScript object

//     // Access current_passage after data is fetched
//     const current_passage = reading_passages[0]["text"];
//     console.log("current_passage in fetchPassages", current_passage)
//     return current_passage; // Now this will work as expected
//     } catch (error) {
//     console.error('Error fetching the JSON file:', error);
//     }
// }

// async function main(){
//     // Call the function
//     current_passage = await fetchPassages();
//     console.log("current_passage in main", current_passage)

//     const parser = new DOMParser()
//     const doc = parser.parseFromString(current_passage, 'text/html')
//     const paragraphs = doc.querySelectorAll('p')
//     const text_passage_display = document.getElementById("textPassage")
//     text_passage_display.innerHTML = "";
//     paragraphs.forEach(p => {
//     const newParagraph = document.createElement('p');
//     newParagraph.textContent = p.textContent;
//     text_passage_display.appendChild(newParagraph);
//     })
// }
// main()

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

async function main() {
    // Fetch and display the first passage initially
    const firstPassage = await fetchPassages();
    if (firstPassage) {
        displayPassage(firstPassage);
    }
}

main();
