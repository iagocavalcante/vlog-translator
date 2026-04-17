import type { NextApiRequest, NextApiResponse } from 'next'
import { spawn } from 'child_process'
import fs from 'fs'
import path from 'path'
import { transferChildProcessOutput } from '../../utils/shell'

export default function GET(
  request: NextApiRequest,
  response: NextApiResponse
) {
  const filePath = request.query.path as string
  if (typeof filePath !== 'string' || !filePath) {
    response.status(400).json({ error: 'Missing "path" query parameter' })
    return
  }

  if (!path.isAbsolute(filePath)) {
    response.status(400).json({ error: 'Path must be absolute' })
    return
  }

  if (!fs.existsSync(filePath)) {
    response.status(400).json({ error: `File not found: ${filePath}` })
    return
  }

  console.log('local transcribe:', filePath)
  const cmd = spawn(
    'python3',
    [path.join(process.cwd(), 'scripts/local-transcribe.py'), filePath],
    { cwd: process.cwd() }
  )
  transferChildProcessOutput(cmd, response)
}
