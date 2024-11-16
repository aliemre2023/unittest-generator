# Unit Test Generator Project
Effortlessly automate unit test creation using AI tools like GitHub Copilot, Python automation, and advanced debugging techniques.

<h3>Inroduction</h3>
Creating unit tests can be repetitive and time-consuming. This project automates the process using GitHub Copilot and Python, significantly improving productivity and reducing manual effort.
By integrating automation tools like PyAutoGUI, this solution interacts with IDEs and generates test files efficiently while ensuring the required libraries and frameworks are properly synchronized.

<h3>Features</h3>
<ul>
  <li>
    <strong>Automated Unit Test Creation:</strong> 
    Generate unit tests with minimal manual intervention.
  </li>
  <li>
    <strong>Integration with GitHub Copilot:</strong> 
    Seamless interaction with Copilot for intelligent code suggestions.
  </li>
  <li>
    <strong>Library Synchronization:</strong> 
    Automatically resolves missing dependencies in generated tests.
  </li>
  <li>
    <strong>Debugging Support:</strong> 
    Adjusts and corrects test files using custom functions.
  </li>
  <li>
    <strong>JUnit Report Parsing:</strong> 
    Extracts and organizes failed test details for easy debugging.
  </li>
</ul>


<h3>Technologies Used</h3>
<ul>
  <li>
    <strong>Languages:</strong> 
    Python
  </li>
  <li>
    <strong>Libraries:</strong>
    <ul>
      <li>PyAutoGUI</li>
      <li>Regular Expressions</li>
      <li>ElementTree</li>
    </ul>
  </li>
  <li>
    <strong>IDEs:</strong> 
    IntelliJ IDEA, Eclipse
  </li>
  <li>
    <strong>Testing Frameworks:</strong> 
    JUnit, PowerMockito
  </li>
</ul>

<h3>Installation</h3>
<ol>
  <li>
    <strong>Clone the repository:</strong>
    <pre><code>git clone https://github.com/aliemre2023/unittest-generator.git</code></pre>
  </li>
  <li>
    <strong>Install the required Python libraries:</strong>
    <pre><code>pip install pyautogui</code></pre>
  </li>
  <li>
    <strong>Set up your IDEs (IntelliJ IDEA and Eclipse) and configure GitHub Copilot.</strong>
  </li>
</ol>

<h3>Usage</h3>
<ul>
  <li>
    <strong>Run the Script:</strong>
    <p>Execute the automation script to start generating unit tests:</p>
    <pre><code>python main_chatVers.py</code></pre>
  </li>
  <li>
    <strong>Generate Prompts:</strong>
    <p>Prompts are created using the <code>prompt_maker</code> function. Automatically fetches suggestions from GitHub Copilot.</p>
  </li>
  <li>
    <strong>Debugging and Library Synchronization:</strong>
    <p>Use <code>debug_PowerMockito</code> to fix method prefixes. Ensure all required libraries are included with <code>library_synchronizer_file</code>.</p>
  </li>
  <li>
    <strong>JUnit Report Parsing:</strong>
    <p>Parse the report to identify and manage failed tests:</p>
    <pre><code>parse_junit_report('modules/junit_reports/junit_report.xml')</code></pre>
  </li>
</ul>

<h3>Acknowledgments</h3>
<ul>
  <li>Special thanks to the Akbank Compass Team for their invaluable support and feedback during this internship project.</li>
</ul>






