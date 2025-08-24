import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [groups, setGroups] = useState([])
  const [students, setStudents] = useState([])
  const [selectedStage, setSelectedStage] = useState('')
  const [showBookingForm, setShowBookingForm] = useState(false)
  const [selectedGroup, setSelectedGroup] = useState(null)
  const [studentData, setStudentData] = useState({
    full_name: '',
    email: '',
    phone: '',
    birth_date: '',
    stage: '',
    notes: ''
  })
  const [showPrimaryOptions, setShowPrimaryOptions] = useState(false)
  const [showPrepOptions, setShowPrepOptions] = useState(false)

  useEffect(() => {
    fetchGroups()
  }, [])

  const fetchGroups = () => {
    fetch('http://127.0.0.1:8000/api/groups/')
      .then(response => response.json())
      .then(data => setGroups(data))
      .catch(error => console.error('Error fetching groups:', error))
  }

  const filteredGroups = selectedStage
    ? groups.filter(group => {
      if (selectedStage === 'SIX_PRIMARY') return group.name.includes('سادس') || group.name.includes('ابتدائي')
      if (selectedStage === 'FIRST_PREP') return group.name.includes('أول') || group.name.includes('إعدادي')
      if (selectedStage === 'SECOND_PREP') return group.name.includes('ثاني') || group.name.includes('إعدادي')
      if (selectedStage === 'THIRD_PREP') return group.name.includes('ثالث') || group.name.includes('إعدادي')
      return true
    })
    : groups

  const handleBookClick = (group) => {
    setSelectedGroup(group)
    setStudentData(prev => ({
      ...prev,
      stage: selectedStage,
      notes: `الصف: ${getStageName(selectedStage)}`
    }))
    setShowBookingForm(true)
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setStudentData(prev => ({ ...prev, [name]: value }))
  }

  const getStageName = (stage) => {
    switch (stage) {
      case 'SIX_PRIMARY': return 'الصف السادس الابتدائي';
      case 'FIRST_PREP': return 'الصف الأول الإعدادي';
      case 'SECOND_PREP': return 'الصف الثاني الإعدادي';
      case 'THIRD_PREP': return 'الصف الثالث الإعدادي';
      default: return '';
    }
  }

  const handleStageSelect = (stage) => {
    setSelectedStage(stage)
    setShowPrimaryOptions(false)
    setShowPrepOptions(false)
  }

  const handleSubmitBooking = async (e) => {
    e.preventDefault()

    try {
      const studentResponse = await fetch('http://127.0.0.1:8000/api/students/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studentData)
      })

      if (!studentResponse.ok) {
        throw new Error('Failed to create student')
      }

      const student = await studentResponse.json()

      const bookingResponse = await fetch('http://127.0.0.1:8000/api/bookings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student: student.id,
          group: selectedGroup.id
        })
      })

      if (bookingResponse.ok) {
        alert('تم الحجز بنجاح!')
        setShowBookingForm(false)
        setStudentData({
          full_name: '',
          email: '',
          phone: '',
          birth_date: '',
          stage: '',
          notes: ''
        })
        fetchGroups()
      } else {
        const errorData = await bookingResponse.json()
        alert(`خطأ في الحجز: ${JSON.stringify(errorData)}`)
      }

    } catch (error) {
      console.error('Error:', error)
      alert('حدث خطأ أثناء الحجز')
    }
  }

  if (showBookingForm) {
    return (
      <div className="booking-form-container">
        <div className="booking-form">
          <h2>حجز في مجموعة {selectedGroup.name}</h2>
          <form onSubmit={handleSubmitBooking}>
            <div className="form-group">
              <label>الاسم بالكامل:</label>
              <input
                type="text"
                name="full_name"
                value={studentData.full_name}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>البريد الإلكتروني:</label>
              <input
                type="email"
                name="email"
                value={studentData.email}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label>رقم الهاتف:</label>
              <input
                type="tel"
                name="phone"
                value={studentData.phone}
                onChange={handleInputChange}
                required
                placeholder="+201234567890"
              />
            </div>

            <div className="form-group">
              <label>تاريخ الميلاد:</label>
              <input
                type="date"
                name="birth_date"
                value={studentData.birth_date}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label>المرحلة الدراسية:</label>
              <input
                type="text"
                value={getStageName(studentData.stage)}
                readOnly
                className="read-only-input"
              />
            </div>

            <div className="form-group">
              <label>ملاحظات (اختياري):</label>
              <textarea
                name="notes"
                value={studentData.notes}
                onChange={handleInputChange}
                placeholder="أي معلومات إضافية تريد إضافتها"
              />
            </div>

            <div className="form-buttons">
              <button type="submit">تأكيد الحجز</button>
              <button type="button" onClick={() => setShowBookingForm(false)}>
                إلغاء
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>نظام حجز دروس اللغة الإنجليزية</h1>
        <p>اختر مجموعتك واحجز مكانك الآن</p>
      </header>

      <main>
        <section className="stage-selection">
          <h2>اختر مرحلتك الدراسية:</h2>
          <div className="stage-buttons">
            <div className="dropdown">
              <button
                onClick={() => {
                  setShowPrimaryOptions(!showPrimaryOptions)
                  setShowPrepOptions(false)
                }}
                className={selectedStage.includes('PRIMARY') ? 'active' : ''}
              >
                المرحلة الابتدائية
                <span className="dropdown-arrow">▼</span>
              </button>
              {showPrimaryOptions && (
                <div className="dropdown-menu">
                  <button onClick={() => handleStageSelect('SIX_PRIMARY')}>
                    الصف السادس الابتدائي
                  </button>
                </div>
              )}
            </div>

            <div className="dropdown">
              <button
                onClick={() => {
                  setShowPrepOptions(!showPrepOptions)
                  setShowPrimaryOptions(false)
                }}
                className={selectedStage.includes('PREP') ? 'active' : ''}
              >
                المرحلة الإعدادية
                <span className="dropdown-arrow">▼</span>
              </button>
              {showPrepOptions && (
                <div className="dropdown-menu">
                  <button onClick={() => handleStageSelect('FIRST_PREP')}>
                    الصف الأول الإعدادي
                  </button>
                  <button onClick={() => handleStageSelect('SECOND_PREP')}>
                    الصف الثاني الإعدادي
                  </button>
                  <button onClick={() => handleStageSelect('THIRD_PREP')}>
                    الصف الثالث الإعدادي
                  </button>
                </div>
              )}
            </div>
          </div>

          {selectedStage && (
            <div className="selected-stage">
              <p>المحدد: <strong>{getStageName(selectedStage)}</strong></p>
              <button
                onClick={() => setSelectedStage('')}
                className="clear-selection"
              >
                ✕ مسح الاختيار
              </button>
            </div>
          )}
        </section>

        <section className="groups-list">
          <h2>المجموعات المتاحة {selectedStage && `للصف ${getStageName(selectedStage)}`}</h2>
          <div className="groups-container">
            {filteredGroups.map(group => (
              <div key={group.id} className="group-card">
                <h3>{group.name}</h3>
                <p>الموعد: {group.schedule}</p>
                <p>الأيام: {group.days}</p>
                <p>السعة: {group.students?.length || 0}/{group.capacity}</p>
                <p className={group.students?.length >= group.capacity ? 'full' : 'available'}>
                  {group.students?.length >= group.capacity ? 'مكتمل' : 'متاح'}
                </p>
                <button
                  onClick={() => handleBookClick(group)}
                  disabled={group.students?.length >= group.capacity}
                >
                  {group.students?.length >= group.capacity ? 'مكتمل' : 'احجز الآن'}
                </button>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App