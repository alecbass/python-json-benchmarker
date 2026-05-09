import { useEffect, useState } from "react";
import { Code, Deck, Fragment, Slide } from "@revealjs/react";
import Reveal from "reveal.js";
import Markdown from "reveal.js/plugin/markdown";
import RevealHighlight from "reveal.js/plugin/highlight";

import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Deck plugins={[Markdown, RevealHighlight]}>
      <Slide>
        <h1>My Cool Talk</h1>
        <p>:)</p>
        <Fragment as="p">First point</Fragment>
        <Fragment as="p">Second point</Fragment>
        <Fragment asChild>
          <p>Third point</p>
        </Fragment>
      </Slide>

      <Slide background="#111827">
        <h2>Second slide</h2>
        <Code language="javascript">
          {`const greeting = 'Hello, world!';
console.log(greeting);`}
        </Code>
      </Slide>

      <Slide>
        <p>Chapter One</p>
        <h1>The Beginning</h1>
        {/* TODO(alec): Come up with a story */}
      </Slide>

      <Slide>
        <h1>Me</h1>
        <p>Me!</p>
        <ul>
          <Fragment as="li">Python + TypeScript + Rust (sometimes)</Fragment>
          <Fragment as="li">Mostly in web development</Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>Interests</p>
        <ul>
          <Fragment as="li">Developer experience</Fragment>
          <Fragment as="li">Optimisation</Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>What this talk is</p>
        <ul>
          <Fragment as="li">
            How Python performance can be increased through native code
          </Fragment>
          <Fragment as="li">
            Whether you should use native code in your Python library
          </Fragment>
          <Fragment as="li">Drawbacks to each approach</Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>
          What this talk is <b>NOT</b>
        </p>
        <ul>
          <Fragment as="li">How to write good Rust</Fragment>
          <Fragment as="li">
            Giving a concrete yes/no as to whether you should use it
          </Fragment>
        </ul>
      </Slide>

      <Slide>
        <h1>Language Comparisons</h1>
        <p>What is native code?</p>
        <ul>
          <Fragment as="li">Code which runs directly as machine code</Fragment>
          <Fragment as="li">
            Often written in languages such as C, C++, Rust, Go etc.
          </Fragment>
          <Fragment as="li">
            Platform-specific - dependent on processor architecture, operating
            system
          </Fragment>
        </ul>
      </Slide>

      <Slide>
        <h1>Different type of programming languages</h1>
      </Slide>

      <Slide>
        <h1>The core: Assembly (machine code)</h1>
        <Code language="assembly">{`mv r16, r17`}</Code>
      </Slide>

      <Slide>
        <h1>Ahead of time compilation: Assembly</h1>
        {/* TODO(alec): Show photos of C, C++, Rust, Go, Zig */}
      </Slide>

      <Slide>
        <h1>Ahead of time compilation: Bytecode</h1>
        {/* TODO(alec): Show photos of Java and C# */}
      </Slide>

      <Slide>
        <h1>Just in time compilation</h1>
        {/* TODO(alec): Show photos of Python and JavaScript */}
      </Slide>

      <Slide>
        <h1>Software with performance constraints</h1>
        <ul>
          <li>Industrial mathematics</li>
          <li>Embedded software</li>
          <li>Databases</li>
          <li>Operating systems</li>
        </ul>
      </Slide>

      <Slide>
        <h1>Commercial Python</h1>
        <ul>
          <li>Lots of stuff, honestly</li>
          <li>Scripting</li>
          <li>Web development</li>
          <li>Scientific Research</li>
          <li>Artificial Intelligence</li>
        </ul>
      </Slide>

      <Slide>
        <p>Chapter Three</p>
        <h1>The Task</h1>
      </Slide>

      <Slide>
        <p>Read in large amounts of JSON data each day</p>
        <p>The constraints:</p>
        <ul>
          <Fragment as="li">Running on a tiny computer</Fragment>
          <Fragment as="li">
            Information needed to reflect realtime ASAP
          </Fragment>
          <Fragment as="li">
            All data was contained within a large (&gt;25GB) .json file
          </Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>My initial approach: read the whole file! (don't do this)</p>
        <Fragment as="p">
          What I ended up doing: stream the file and parse it using the{" "}
          <b>ijson</b> library
          {/* TODO(alec): Show photos of C, C++, Rust, Go, Zig */}
          <Code language="python">
            {`import ijson

# Open the JSON file
with open('large_file.json', 'r') as file:
    # Parse the JSON objects one by one
    parser = ijson.items(file, 'item')

    # Iterate over the JSON objects
    for item in parser:
        # Process each JSON object as needed
        print(item)`}
          </Code>
          <span>
            Source:
            <a href="">
              https://medium.com/@AlexanderObregon/json-streaming-how-to-work-with-large-json-files-efficiently-c7203de60ac2
            </a>
          </span>
        </Fragment>
      </Slide>

      <Slide>
        <p>My side project: reading it in Rust</p>
        <Fragment as="p">It was actually way faster</Fragment>
        <Fragment as="p">It was a fun learning task</Fragment>
      </Slide>

      <Slide>
        <span>Chapter Four</span>
        <h1>The world's worst JSON parser</h1>
      </Slide>

      <Slide>
        <p>
          The task: write near-identical JSON parser libraries in both Python
          and Rust
        </p>
        <Fragment as="p">
          Caveat: The Rust library must be callable from Python how an end-user
          would use it
        </Fragment>
        <Fragment as="p">Compare the performance</Fragment>
      </Slide>

      <Slide>
        <p>
          The approach: Read a file character-by-character, and make each items
          avaiable through an interator when available
        </p>
        <Code language="python">
          {`python_chunked_reader = PythonChunkedReader.create(file_path, 20)
    while True:
        try:
            items = next(python_chunked_reader)
            for item in items:
                print(item)
        except StopIteration:
            break`}
        </Code>
      </Slide>

      <Slide>
        <p>How do I actually call the Rust function from Python?</p>
        <Fragment as="p">
          The <b>maturin</b> library
        </Fragment>
        <Fragment as="p">
          Takes in Rust code, compiles it using the <b>pyo3</b> library and
          turns it into a Python wheel (pre-built package)
        </Fragment>
      </Slide>

      <Slide>{/* TODO(alec): Insert the Python code vs Rust */}</Slide>

      <Slide>
        <p>Performance</p>
        <ul>
          <Fragment as="li">
            Python code took <b>80s</b> to run
          </Fragment>
          <Fragment as="li">
            Rust code took <b>3s</b> to run
          </Fragment>
        </ul>
        <Fragment as="p">But why???</Fragment>
      </Slide>

      <Slide>
        <p>Python vs Rust</p>
        {/* TODO(alec): AOT compiled vs JIT, garbage collected */}
        {/* TODO(alec): Show assembly if possible? */}
      </Slide>

      <Slide>
        <h1>Advantages</h1>
        <ul>
          <li>Direct machine code</li>
          <li>Typing</li>
        </ul>
      </Slide>

      <Slide>
        <p>Advantages: Machine code</p>
        <p>Pre-optimised</p>
        <p>Faster code execution</p>
      </Slide>

      <Slide>
        <p>Advantages: Typing</p>
      </Slide>

      <Slide>
        <p>Advantages: Typing</p>
        {/* TODO(alec): Show Rust double() function example and how the types will always match */}
        <ul>
          <li>Can't pass in invalid parameter to functions</li>
          <li>
            Function takes in a string? It <b>WILL</b> be a string at runtime
          </li>
        </ul>
      </Slide>

      <Slide>
        <h1>It's not all binkies and blankets</h1>
      </Slide>

      <Slide>
        <p>Disadvantages</p>
        {/* TODO(alec): Show python double() function example and how type hints don't actually do anything */}
        <ul>
          <li>Typing</li>
          <li>Being across two languages</li>
          <li>Platform dependency</li>
        </ul>
      </Slide>

      <Slide>
        <p>Disadvantages: Typing</p>
        <p>This one is specific to Maturin and Pyo3</p>
        <p>How do you write type hints for Python developers?</p>
        {/* TODO(alec): Show python double() function example and how type hints don't actually do anything */}
      </Slide>

      <Slide>
        <p>Disadvantages: Typing</p>
        <p>Option one: Write them yourself</p>
        <p>Option two: Use a library (this one uses pyo3-stub-gen</p>
        {/* TODO(alec): Show Rust struct and impl block and the json_benchmarker.pyi file */}
      </Slide>

      <Slide>
        <p>Disadvantages: Multi-language</p>
        <p>You now need to be across multiple languages</p>
      </Slide>

      <Slide>
        <p>Disadvantages: Platform dependency</p>
        <ul>
          <Fragment as="li">
            Python is, for the most, part, write-once-run-anywhere
          </Fragment>
          <Fragment as="li">
            Machine code is specific to processor achitecture operating system
          </Fragment>
          <Fragment as="li">
            Use a Linux-specific API? Goodbye Window and Mac users
          </Fragment>
        </ul>
      </Slide>

      <Slide>
        <p>
          Why not use the <b>ijson</b> library like in the work example
        </p>
        <Fragment as="p">
          The two libraries should have had business logic as similar as
          possible, to measure performance differences
        </Fragment>
        <Fragment as="p">
          Depending on how you use it, <b>ijson</b> itself uses functionality
          written in C
        </Fragment>
      </Slide>

      <Slide>
        <p>Why doesn't everyone use native code?</p>
        {/* TODO(alec): Show Python reading file by line vs C example */}
        <Fragment as="p">
          For most modern software projects, it doesn't matter
        </Fragment>
        <Fragment as="p">Example: Web development</Fragment>
        <Fragment as="p">
          A slow database query or network latency in an endpoint will slow you
          down more than Python vs native
        </Fragment>
        <Fragment as="p">
          10ms vs 50ms for a function call doesn't matter if someone uploads a
          file over 3G
        </Fragment>
      </Slide>

      <Slide>
        <h1>Thoughts? Concerns? Feelings?</h1>
      </Slide>
    </Deck>
  );
}

export default App;
