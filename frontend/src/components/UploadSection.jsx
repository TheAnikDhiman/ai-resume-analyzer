import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X } from 'lucide-react'

export default function UploadSection({ onFileSelect, onJDChange, onAnalyze, loading }) {
  const [file, setFile] = useState(null)
  const [jd, setJd] = useState('')

  const onDrop = useCallback((acceptedFiles) => {
    const selected = acceptedFiles[0]
    if (selected) {
      setFile(selected)
      onFileSelect(selected)
    }
  }, [onFileSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1
  })

  const removeFile = () => {
    setFile(null)
    onFileSelect(null)
  }

  return (
    <div className="space-y-6">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-300
          ${isDragActive
            ? 'border-blue-500 bg-blue-500/10'
            : 'border-gray-700 hover:border-blue-500 hover:bg-blue-500/5'
          }`}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto mb-4 text-blue-400" size={40} />
        {isDragActive ? (
          <p className="text-blue-400 font-medium">Drop your resume here...</p>
        ) : (
          <>
            <p className="text-gray-300 font-medium text-lg">Drag & drop your resume</p>
            <p className="text-gray-500 text-sm mt-1">or click to browse — PDF only</p>
          </>
        )}
      </div>

      {/* File selected */}
      {file && (
        <div className="flex items-center justify-between bg-gray-800 rounded-xl px-4 py-3 border border-gray-700">
          <div className="flex items-center gap-3">
            <FileText size={20} className="text-blue-400" />
            <span className="text-gray-200 text-sm font-medium">{file.name}</span>
            <span className="text-gray-500 text-xs">
              {(file.size / 1024).toFixed(1)} KB
            </span>
          </div>
          <button onClick={removeFile} className="text-gray-500 hover:text-red-400 transition">
            <X size={18} />
          </button>
        </div>
      )}

      {/* JD Input */}
      <div>
        <label className="text-gray-400 text-sm font-medium block mb-2">
          Job Description <span className="text-gray-600">(optional — for targeted analysis)</span>
        </label>
        <textarea
          rows={5}
          value={jd}
          onChange={(e) => { setJd(e.target.value); onJDChange(e.target.value) }}
          placeholder="Paste the job description here to get a targeted JD match score..."
          className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-gray-300
                     text-sm placeholder-gray-600 focus:outline-none focus:border-blue-500
                     resize-none transition"
        />
      </div>

      {/* Analyze Button */}
      <button
        onClick={onAnalyze}
        disabled={!file || loading}
        className={`w-full py-4 rounded-xl font-semibold text-base tracking-wide transition-all duration-300
          ${!file || loading
            ? 'bg-gray-800 text-gray-600 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40'
          }`}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-3">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            Analyzing Resume...
          </span>
        ) : (
          '🔍 Analyze Resume'
        )}
      </button>
    </div>
  )
}