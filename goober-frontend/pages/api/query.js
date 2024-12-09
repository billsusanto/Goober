import { spawn } from 'child_process';
import path from 'path';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }

    const scriptPath = path.join(process.cwd(), 'utils/query.py');
    console.log('Resolved Python script path:', scriptPath);

    try {
      const results = await new Promise((resolve, reject) => {
        const process = spawn('python', [scriptPath]);
        let output = '';
        let errorOutput = '';

        // Capture stdout and stderr
        process.stdout.on('data', (data) => {
          output += data.toString();
        });

        process.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        // Handle process close
        process.on('close', (code) => {
          if (code !== 0 || errorOutput) {
            console.error(`Python error: ${errorOutput}`);
            reject(new Error('Python script execution failed'));
          } else {
            const results = output.split('\n').filter((line) => line.trim() !== '');
            resolve(results);
          }
        });

        // Send input to Python script
        process.stdin.write(query + '\n');
        process.stdin.end();
      });

      res.status(200).json(results);
    } catch (error) {
      console.error('Error in API handler:', error.message);
      res.status(500).json({ error: 'Internal server error', details: error.message });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
