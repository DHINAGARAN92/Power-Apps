let entities = {};

document.addEventListener("DOMContentLoaded", function () {
  const importButton = document.getElementById("import-zip");
  const fileInput = document.getElementById("file-input");
  const fileNameDisplay = document.getElementById("file-name");
  const dashboard = document.getElementById("dashboard");
  const entityDetails = document.getElementById("entity-details");

  // Handle import button click
  importButton.addEventListener("click", () => fileInput.click());

  // Handle file input change
  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (file) {
      fileNameDisplay.textContent = `Selected File: ${file.name}`;
      await processZipFile(file);
    }
  });

  // Navigation: Home
  document.getElementById("menu-home").addEventListener("click", () => {
    dashboard.style.display = "block";
    entityDetails.style.display = "none";
  });

  // Navigation: Entity Details
  document.getElementById("menu-entities").addEventListener("click", () => {
    dashboard.style.display = "none";
    entityDetails.style.display = "block";
  });
});

// Process ZIP file
async function processZipFile(file) {
  const jszip = new JSZip();
  const zipContent = await jszip.loadAsync(file);
  const xmlContent = await zipContent.files["customizations.xml"].async("string");
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(xmlContent, "text/xml");

  // Extract Canvas App details
  const appName = xmlDoc.querySelector("CanvasApp > DisplayName")?.textContent || "N/A";
  const appVersion = xmlDoc.querySelector("CanvasApp > AppVersion")?.textContent || "N/A";
  const appStatus = xmlDoc.querySelector("CanvasApp > Status")?.textContent || "N/A";

  const canvasAppDetailsHTML = `
    <p><strong>App Name:</strong> ${appName}</p>
    <p><strong>Version:</strong> ${appVersion}</p>
    <p><strong>Status:</strong> ${appStatus}</p>`;
  document.getElementById("canvas-app-details").innerHTML = canvasAppDetailsHTML;

  // Extract entities and their attributes
  const entityNodes = xmlDoc.querySelectorAll("Entity");
  entities = {};
  entityNodes.forEach((entity) => {
    const entityName =
      entity.querySelector("Name[LocalizedName]")?.getAttribute("LocalizedName") || "N/A";
    const attributes = Array.from(entity.querySelectorAll("attributes > attribute")).map((attr) => ({
      name: attr.querySelector("Name")?.textContent || "N/A",
      type: attr.querySelector("Type")?.textContent || "N/A",
      required: attr.querySelector("RequiredLevel")?.textContent || "N/A",
      displayName: attr.querySelector("displayname")?.getAttribute("description") || "N/A",
      isCustom: attr.querySelector("IsCustomField")?.textContent === "1",
    }));
    entities[entityName] = attributes;
  });

  populateEntityDropdown();
}

// Populate entity dropdown
function populateEntityDropdown() {
  const dropdownContainer = document.getElementById("dropdown-container");
  let dropdownHTML = '<select id="entitySelect" onchange="displayAttributes()">';
  dropdownHTML += '<option value="">--Select Entity--</option>';
  Object.keys(entities).forEach((entityName) => {
    dropdownHTML += `<option value="${entityName}">${entityName}</option>`;
  });
  dropdownContainer.innerHTML = dropdownHTML;
}

// Display entity attributes
function displayAttributes() {
  const selectedEntity = document.getElementById("entitySelect").value;
  const outputDiv = document.getElementById("output");

  if (!selectedEntity || !entities[selectedEntity]) {
    outputDiv.innerHTML = "";
    return;
  }

  const attributes = entities[selectedEntity];
  let html = `<h3>Attributes for ${selectedEntity}</h3>
              <table>
                <thead>
                  <tr>
                    <th>Display Name<br><input type="text" onkeyup="filterTable(0)" placeholder="Filter by display"></th>
                    <th>Attribute Name<br><input type="text" onkeyup="filterTable(1)" placeholder="Filter by name"></th>
                    <th>Type<br><input type="text" onkeyup="filterTable(2)" placeholder="Filter by type"></th>
                    <th>Required<br><input type="text" onkeyup="filterTable(3)" placeholder="Filter by required"></th>
                    <th>Column Type<br><input type="text" onkeyup="filterTable(4)" placeholder="Filter by type"></th>
                  </tr>
                </thead>
                <tbody>`;

  attributes.forEach((attr) => {
    html += `<tr>
                <td>${attr.displayName}</td>
                <td>${attr.name}</td>
                <td>${attr.type}</td>
                <td>${attr.required}</td>
                <td>${attr.isCustom ? "User-Created" : "Default"}</td>
             </tr>`;
  });

  html += "</tbody></table>";
  outputDiv.innerHTML = html;
}

// Filter table by column
function filterTable(columnIndex) {
  const input = event.target;
  const filter = input.value.toLowerCase();
  const table = document.querySelector("#output table");
  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    const cell = rows[i].getElementsByTagName("td")[columnIndex];
    if (cell) {
      const textValue = cell.textContent || cell.innerText;
      rows[i].style.display = textValue.toLowerCase().includes(filter) ? "" : "none";
    }
  }
}
