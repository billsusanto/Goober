import { spawn } from 'child_process';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { query } = req.body;

    // Wrap the Python script execution in a Promise
    return new Promise((resolve, reject) => {
      const process = spawn('python', ['pages/api/query.py']);
      let output = '';
      let errorOutput = '';

      // Capture stdout data
      process.stdout.on('data', (data) => {
        output += data.toString();
      });

      // Capture stderr data
      process.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      // Handle process close
      process.on('close', (code) => {
        if (code !== 0 || errorOutput) {
          console.error(`Error output from query.py: ${errorOutput}`);
          res.status(500).json({ error: 'Error in Python script', details: errorOutput });
          reject(new Error('Python script execution failed'));
          return;
        }

        const results = output.split('\n').filter(line => line.trim() !== '');
        res.status(200).json(results);
        resolve();
      });

      // Send the input to the Python script
      process.stdin.write(query + '\n');
      process.stdin.end();
    });
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
