/**
 * Generate selected V/F variables
 */
function gatLetters() {
    let formula = document.getElementById("formulaInput").value;
    let arrayLetters = extractLetters(formula);

    let variableCard = document.getElementById("variableCard");
    variableCard.style.display = "block";

    let variablesContainer = document.getElementById("variablesContainer");
    variablesContainer.innerHTML = "";

    arrayLetters.forEach(element => {
        let newItem = `<div class="col-md-4 mb-1">
                            <div class="form-floating">
                                <select class="form-select" id="value_${element}" aria-label="Floating label select example">
                                    <option selected>V/F</option>
                                    <option value="V">V</option>
                                    <option value="F">F</option>
                                </select>
                                <label for="value_${element}">${element}</label>
                            </div>
                        </div>`;
        
        variablesContainer.innerHTML += newItem;
    });
}

/**
 * Return or sets an array of non-repeating letters
 * @param {*} formula 
 * @returns Array of letters
 */
function extractLetters(formula) {

    // Response array of non-repeating letters
    let letters = new Array();

    // An array of letters is obtained from the formula using regular expressions
    let purgeFormula = formula.match(/[a-zA-Z]/g);

    for (let index = 0; index < purgeFormula.length; index++) {
        const element = purgeFormula[index];

        // Push in array only letters not included
        if (!letters.includes(element)) {
            letters.push(element);
        }
    }

    return letters;
}