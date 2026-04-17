import Head from 'next/head'
import { styled } from '../stitches.config'
import { Box } from '../components/box'
import { Output } from '../components/output'
import { VideoForm } from '../components/video-form'
import { LocalFileForm } from '../components/local-file-form'
import {
  TabsContent,
  TabsList,
  TabsRoot,
  TabsTrigger
} from '../components/tabs'
import { useState } from 'react'
import {
  extractVideoIdFromUrl,
  processLocalFile,
  processVideo
} from '../utils/api-client'

const Text = styled('p', {
  fontFamily: '$system',
  color: '$hiContrast'
})

const Container = styled('div', {
  display: 'flex',
  flexDirection: 'column',
  height: '100vh',
  marginY: 0,
  marginX: 'auto',
  paddingX: '$3',
  paddingY: 0,

  variants: {
    size: {
      1: {
        maxWidth: '300px'
      },
      2: {
        maxWidth: '585px'
      },
      3: {
        maxWidth: '865px'
      }
    }
  }
})

export default function Home() {
  const [isProcessing, setProcessing] = useState(false)
  const [progressOutput, setProgressOutput] = useState('')
  const [activeTab, setActiveTab] = useState('progress')
  const [sourceTab, setSourceTab] = useState('youtube')
  const [resultTranscript, setResultTranscript] = useState('')

  const runProcessing = async (task: () => Promise<string | false>) => {
    setResultTranscript('')
    setProcessing(true)

    const translated = await task()
    if (translated) {
      setResultTranscript(translated)
    }

    setProcessing(false)
    setActiveTab('result')
  }

  const handleYouTubeSubmit = async (videoUrl: string) => {
    let videoId: string | null
    try {
      videoId = extractVideoIdFromUrl(videoUrl)
    } catch {
      alert('Invalid URL')
      return
    }
    if (!videoId) {
      alert('Invalid URL')
      return
    }

    await runProcessing(() =>
      processVideo(videoId as string, message => {
        setProgressOutput(prev => prev + message)
      })
    )
  }

  const handleLocalFileSubmit = async (filePath: string) => {
    if (!filePath) {
      alert('Please enter a file path')
      return
    }

    await runProcessing(() =>
      processLocalFile(filePath, message => {
        setProgressOutput(prev => prev + message)
      })
    )
  }

  return (
    <Box css={{ paddingY: '$6' }}>
      <Head>
        <title>Vlog Transcription &amp; Brazilian Portuguese Translation</title>
      </Head>
      <Container size={{ '@initial': '1', '@bp1': '2' }}>
        <Text as="h1">
          Vlog Transcription &amp; Brazilian Portuguese Translation Tool
        </Text>
        <TabsRoot value={sourceTab} onValueChange={setSourceTab}>
          <TabsList aria-label="Source">
            <TabsTrigger value="youtube">YouTube</TabsTrigger>
            <TabsTrigger value="local">Local file</TabsTrigger>
          </TabsList>
          <TabsContent value="youtube">
            <Box css={{ paddingTop: '$3' }}>
              <VideoForm
                onSubmit={handleYouTubeSubmit}
                isProcessing={isProcessing}
              />
            </Box>
          </TabsContent>
          <TabsContent value="local">
            <Box css={{ paddingTop: '$3' }}>
              <LocalFileForm
                onSubmit={handleLocalFileSubmit}
                isProcessing={isProcessing}
              />
            </Box>
          </TabsContent>
        </TabsRoot>
        <TabsRoot value={activeTab} onValueChange={setActiveTab}>
          <TabsList aria-label="Output">
            <TabsTrigger value="progress">Progress</TabsTrigger>
            <TabsTrigger value="result">Result</TabsTrigger>
          </TabsList>
          <TabsContent value="progress">
            <Output>{progressOutput}</Output>
          </TabsContent>
          <TabsContent value="result">
            <Output>{resultTranscript}</Output>
          </TabsContent>
        </TabsRoot>
      </Container>
    </Box>
  )
}
