import { useState } from 'react'
import axios from 'axios'
import UploadSection from './components/UploadSection'
import ResultsDashboard from './components/ResultsDashboard'
import { FileSearch } from 'lucide-react'

export default function App() {
  const [file, setFile] = useState(null)
  const [jdText, setJdText] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('jd_text', jdText)
      const res = await axios.post('http://localhost:8000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResults(res.data)
    } catch (err) {
      setError('Something went wrong. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="border-b border-gray-800 bg-gray-900/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center gap-3">
          <FileSearch size={24} className="text-blue-400" />
          <div>
            <h1 className="text-lg font-bold text-white leading-none">
              AI Resume Analyzer
            </h1>
            <p className="text-xs text-gray-500 mt-0.5">
              ATS Score Checker Using NLP
            </p>
          </div>
          <span className="ml-auto text-xs bg-blue-500/10 border border-blue-500/20 text-blue-400 px-3 py-1 rounded-full font-medium">
            BCA Final Project
          </span>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-10">
        <div className="text-center mb-10">
          <h2 className="text-4xl font-bold text-white mb-3">
            Is your resume{' '}
            <span className="text-blue-400">ATS ready?</span>
          </h2>
          <p className="text-gray-400 text-base max-w-xl mx-auto">
            Upload your resume and instantly find out your ATS score,
            detected skills, missing keywords, and actionable suggestions.
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-2xl">
          <UploadSection
            onFileSelect={setFile}
            onJDChange={setJdText}
            onAnalyze={handleAnalyze}
            loading={loading}
          />

          {error && (
            <div className="mt-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl px-4 py-3 text-sm">
              {error}
            </div>
          )}
          {results && <ResultsDashboard data={{...results, file, jd_text: jdText}} />}
          </div>
        <p className="text-center text-gray-700 text-xs mt-8">
          Built with Python · FastAPI · React · Tailwind CSS · pdfplumber
        </p>
      </div>
    </div>
  )
}