import { RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts'
import { CheckCircle, XCircle, AlertTriangle, Lightbulb } from 'lucide-react'
import { Download } from 'lucide-react'

{/* Download Button */}
      <div className="flex justify-end mb-2">
        <button
          onClick={async () => {
            const formData = new FormData()
            formData.append('file', data.file)
            formData.append('jd_text', data.jd_text || '')
            const res = await fetch('http://localhost:8000/download-report', {
              method: 'POST', body: formData
            })
            const blob = await res.blob()
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = 'ATS_Report.pdf'
            a.click()
          }}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white
                     px-4 py-2 rounded-xl text-sm font-medium transition"
        >
          <Download size={15} /> Download Report
        </button>
      </div>

function ScoreGauge({ score, label, color }) {
  const data = [{ value: score }]
  const ringColor = score >= 70 ? '#22c55e' : score >= 40 ? '#f59e0b' : '#ef4444'

  return (
    <div className="flex flex-col items-center bg-gray-800/60 border border-gray-700 rounded-2xl p-6">
      <p className="text-gray-400 text-sm font-medium mb-2">{label}</p>
      <div className="relative">
        <RadialBarChart
          width={160} height={160}
          cx={80} cy={80}
          innerRadius={55} outerRadius={75}
          startAngle={90} endAngle={-270}
          data={data}
        >
          <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
          <RadialBar
            dataKey="value"
            cornerRadius={10}
            fill={ringColor}
            background={{ fill: '#1f2937' }}
          />
        </RadialBarChart>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold text-white">{score}%</span>
        </div>
      </div>
      <span
        className="mt-3 text-xs font-semibold px-3 py-1 rounded-full"
        style={{ background: `${ringColor}20`, color: ringColor }}
      >
        {score >= 70 ? 'Strong' : score >= 40 ? 'Moderate' : 'Weak'}
      </span>
    </div>
  )
}

function SkillChip({ skill, detected }) {
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium border transition
      ${detected
        ? 'bg-green-500/10 border-green-500/30 text-green-400'
        : 'bg-red-500/10 border-red-500/30 text-red-400'
      }`}>
      {skill}
    </span>
  )
}

export default function ResultsDashboard({ data }) {
  const { ats_score, detected_skills, missing_skills,
          suggestions, found_sections, missing_sections, jd_match } = data

  return (
    <div className="space-y-6 mt-8 animate-fadeIn">

      {/* Score Gauges */}
      <div className={`grid gap-4 ${jd_match ? 'grid-cols-2' : 'grid-cols-1 max-w-xs mx-auto'}`}>
        <ScoreGauge score={ats_score} label="Overall ATS Score" />
        {jd_match && <ScoreGauge score={jd_match.score} label="JD Match Score" />}
      </div>

      {/* JD Match Skills */}
      {jd_match && (
        <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
            🎯 Job Description Match
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-green-400 text-xs font-semibold mb-2 uppercase tracking-wider">
                Matched from JD
              </p>
              <div className="flex flex-wrap gap-2">
                {jd_match.matched.length > 0
                  ? jd_match.matched.map(s => <SkillChip key={s} skill={s} detected />)
                  : <p className="text-gray-600 text-sm">None matched</p>
                }
              </div>
            </div>
            <div>
              <p className="text-red-400 text-xs font-semibold mb-2 uppercase tracking-wider">
                Missing from JD
              </p>
              <div className="flex flex-wrap gap-2">
                {jd_match.missing.length > 0
                  ? jd_match.missing.map(s => <SkillChip key={s} skill={s} detected={false} />)
                  : <p className="text-gray-500 text-sm">All covered! 🎉</p>
                }
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Skills */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6">
          <p className="text-green-400 text-xs font-semibold mb-3 uppercase tracking-wider flex items-center gap-2">
            <CheckCircle size={14} /> Detected Skills ({detected_skills.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {detected_skills.map(s => <SkillChip key={s} skill={s} detected />)}
          </div>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6">
          <p className="text-red-400 text-xs font-semibold mb-3 uppercase tracking-wider flex items-center gap-2">
            <XCircle size={14} /> Missing Skills ({missing_skills.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {missing_skills.map(s => <SkillChip key={s} skill={s} detected={false} />)}
          </div>
        </div>
      </div>

      {/* Section Checker */}
      <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6">
        <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
          🗂️ Resume Section Checker
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-green-400 text-xs font-semibold mb-2 uppercase tracking-wider">Found</p>
            <div className="space-y-1">
              {found_sections.map(s => (
                <div key={s} className="flex items-center gap-2 text-sm text-gray-300">
                  <CheckCircle size={14} className="text-green-400" /> {s}
                </div>
              ))}
            </div>
          </div>
          <div>
            <p className="text-red-400 text-xs font-semibold mb-2 uppercase tracking-wider">Missing</p>
            <div className="space-y-1">
              {missing_sections.length > 0
                ? missing_sections.map(s => (
                    <div key={s} className="flex items-center gap-2 text-sm text-gray-300">
                      <AlertTriangle size={14} className="text-amber-400" /> {s}
                    </div>
                  ))
                : <p className="text-green-400 text-sm">All sections present 🎉</p>
              }
            </div>
          </div>
        </div>
      </div>

      {/* Suggestions */}
      <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6">
        <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
          <Lightbulb size={16} className="text-amber-400" /> Suggestions
        </h3>
        <div className="space-y-3">
          {suggestions.map((tip, i) => (
            <div key={i} className="flex items-start gap-3 bg-gray-900/50 rounded-xl px-4 py-3">
              <span className="text-amber-400 mt-0.5">→</span>
              <p className="text-gray-300 text-sm">{tip}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  )
}