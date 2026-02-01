'use client'
import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Trash2, Plus, Minus, Send, MessageCircle, ArrowLeft, ShoppingCart } from 'lucide-react'
import { useQuote } from '@/context/QuoteContext'

export default function QuotePage() {
  const { quoteItems, removeFromQuote, updateQuantity, clearQuote } = useQuote()
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    message: ''
  })

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const generateWhatsAppMessage = () => {
    let message = `*Request for Quotation*\n\n`
    message += `Name: ${formData.name}\n`
    message += `Email: ${formData.email}\n`
    message += `Phone: ${formData.phone}\n`
    if (formData.company) message += `Company: ${formData.company}\n`
    message += `\n*Products:*\n\n`
    
    quoteItems.forEach((item, index) => {
      message += `${index + 1}. ${item.name}\n`
      message += `   Quantity: ${item.quantity}\n`
      message += `   Price: AED ${item.price.toFixed(2)}\n`
      message += `   Subtotal: AED ${(item.price * item.quantity).toFixed(2)}\n\n`
    })
    
    const total = quoteItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    message += `*Total: AED ${total.toFixed(2)}*\n\n`
    
    if (formData.message) {
      message += `Additional Message:\n${formData.message}`
    }
    
    return message
  }

  const handleWhatsAppSubmit = () => {
    if (!formData.name || !formData.phone) {
      alert('Please fill in Name and Phone number')
      return
    }
    
    const message = generateWhatsAppMessage()
    const whatsappUrl = `https://wa.me/971445222261?text=${encodeURIComponent(message)}`
    window.open(whatsappUrl, '_blank')
    
    setFormData({ name: '', email: '', phone: '', company: '', message: '' })
    clearQuote()
    setShowForm(false)
  }

  const handleEmailSubmit = (e) => {
    e.preventDefault()
    alert('Quote request sent! We will contact you soon.')
    setFormData({ name: '', email: '', phone: '', company: '', message: '' })
    clearQuote()
    setShowForm(false)
  }

  // Empty State
  if (quoteItems.length === 0) {
    return (
      <div className="container mx-auto px-4 py-12 md:py-16">
        <div className="text-center">
          <div className="text-gray-400 mb-4">
            <ShoppingCart size={60} className="mx-auto md:w-20 md:h-20" />
          </div>
          <h2 className="text-2xl md:text-3xl font-bold mb-3 md:mb-4">Your Quote List is Empty</h2>
          <p className="text-gray-600 mb-6 md:mb-8 text-sm md:text-base">Add products to request a quotation</p>
          <Link href="/products">
            <button className="bg-primary text-white px-6 md:px-8 py-2 md:py-3 rounded-lg hover:bg-blue-700 transition text-sm md:text-base">
              Browse Products
            </button>
          </Link>
        </div>
      </div>
    )
  }

  const total = quoteItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  return (
    <div className="bg-gray-50 min-h-screen py-4 md:py-8">
      <div className="container mx-auto px-3 md:px-4">
        {/* Back Button */}
        <Link 
          href="/products" 
          className="inline-flex items-center gap-2 text-primary hover:underline mb-4 md:mb-6 text-sm md:text-base"
        >
          <ArrowLeft size={18} className="md:w-5 md:h-5" />
          Continue Shopping
        </Link>

        {/* Page Title */}
        <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold mb-6 md:mb-8">Request Quotation</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
          {/* Quote Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-4 md:p-6">
              <div className="flex justify-between items-center mb-4 md:mb-6">
                <h2 className="text-lg md:text-xl lg:text-2xl font-bold">
                  Selected Products ({quoteItems.length})
                </h2>
                <button 
                  onClick={clearQuote}
                  className="text-red-500 hover:text-red-700 text-xs md:text-sm"
                >
                  Clear All
                </button>
              </div>

              <div className="space-y-3 md:space-y-4">
                {quoteItems.map((item) => (
                  <div key={item.id} className="flex gap-3 md:gap-4 p-3 md:p-4 border rounded-lg">
                    {/* Product Image */}
                    <div className="relative w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 flex-shrink-0">
                      <Image
                        src={item.image}
                        alt={item.name}
                        fill
                        className="object-cover rounded"
                      />
                    </div>

                    {/* Product Info */}
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold mb-1 text-sm md:text-base line-clamp-2">
                        {item.name}
                      </h3>
                      <p className="text-xs md:text-sm text-gray-600 mb-2">{item.category}</p>
                      <p className="text-base md:text-lg font-bold text-primary">
                        AED {item.price.toFixed(2)}
                      </p>
                      
                      {/* Mobile Quantity Controls */}
                      <div className="flex items-center gap-2 mt-3 md:hidden">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="w-7 h-7 border rounded hover:bg-gray-100 flex items-center justify-center"
                        >
                          <Minus size={14} />
                        </button>
                        <span className="w-10 text-center font-semibold text-sm">{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="w-7 h-7 border rounded hover:bg-gray-100 flex items-center justify-center"
                        >
                          <Plus size={14} />
                        </button>
                        <span className="text-xs text-gray-600 ml-2">
                          AED {(item.price * item.quantity).toFixed(2)}
                        </span>
                      </div>
                    </div>

                    {/* Desktop Quantity & Remove */}
                    <div className="hidden md:flex flex-col items-end justify-between">
                      <button
                        onClick={() => removeFromQuote(item.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 size={20} />
                      </button>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="w-8 h-8 border rounded hover:bg-gray-100 flex items-center justify-center"
                        >
                          <Minus size={16} />
                        </button>
                        <span className="w-12 text-center font-semibold">{item.quantity}</span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="w-8 h-8 border rounded hover:bg-gray-100 flex items-center justify-center"
                        >
                          <Plus size={16} />
                        </button>
                      </div>

                      <p className="text-sm text-gray-600 mt-2">
                        Subtotal: AED {(item.price * item.quantity).toFixed(2)}
                      </p>
                    </div>

                    {/* Mobile Remove Button */}
                    <button
                      onClick={() => removeFromQuote(item.id)}
                      className="md:hidden text-red-500 hover:text-red-700 self-start"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Summary & Form - Sticky on Desktop */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-4 md:p-6 lg:sticky lg:top-24">
              <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">Quote Summary</h2>
              
              <div className="space-y-2 md:space-y-3 mb-4 md:mb-6">
                <div className="flex justify-between text-sm md:text-base">
                  <span className="text-gray-600">Items:</span>
                  <span className="font-semibold">{quoteItems.length}</span>
                </div>
                <div className="flex justify-between text-sm md:text-base">
                  <span className="text-gray-600">Total Quantity:</span>
                  <span className="font-semibold">
                    {quoteItems.reduce((sum, item) => sum + item.quantity, 0)}
                  </span>
                </div>
                <div className="border-t pt-3 flex justify-between text-lg md:text-xl font-bold">
                  <span>Estimated Total:</span>
                  <span className="text-primary">AED {total.toFixed(2)}</span>
                </div>
              </div>

              <p className="text-xs md:text-sm text-gray-600 mb-4 md:mb-6">
                *Final price will be confirmed in the quotation
              </p>

              {!showForm ? (
                <button
                  onClick={() => setShowForm(true)}
                  className="w-full bg-primary text-white py-3 rounded-lg hover:bg-blue-700 transition font-semibold text-sm md:text-base"
                >
                  Request Quotation
                </button>
              ) : (
                <div className="space-y-3 md:space-y-4">
                  <h3 className="font-bold text-base md:text-lg">Your Details</h3>
                  
                  <input
                    type="text"
                    name="name"
                    placeholder="Full Name *"
                    value={formData.name}
                    onChange={handleInputChange}
                    className="w-full px-3 md:px-4 py-2 border rounded-lg focus:outline-none focus:border-primary text-sm md:text-base"
                    required
                  />
                  
                  <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-3 md:px-4 py-2 border rounded-lg focus:outline-none focus:border-primary text-sm md:text-base"
                  />
                  
                  <input
                    type="tel"
                    name="phone"
                    placeholder="Phone Number *"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-3 md:px-4 py-2 border rounded-lg focus:outline-none focus:border-primary text-sm md:text-base"
                    required
                  />
                  
                  <input
                    type="text"
                    name="company"
                    placeholder="Company Name (Optional)"
                    value={formData.company}
                    onChange={handleInputChange}
                    className="w-full px-3 md:px-4 py-2 border rounded-lg focus:outline-none focus:border-primary text-sm md:text-base"
                  />
                  
                  <textarea
                    name="message"
                    placeholder="Additional requirements or questions..."
                    value={formData.message}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-3 md:px-4 py-2 border rounded-lg focus:outline-none focus:border-primary text-sm md:text-base"
                  />

                  <button
                    onClick={handleWhatsAppSubmit}
                    className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition font-semibold flex items-center justify-center gap-2 text-sm md:text-base"
                  >
                    <MessageCircle size={18} className="md:w-5 md:h-5" />
                    Send via WhatsApp
                  </button>

                  <button
                    onClick={handleEmailSubmit}
                    className="w-full bg-primary text-white py-3 rounded-lg hover:bg-blue-700 transition font-semibold flex items-center justify-center gap-2 text-sm md:text-base"
                  >
                    <Send size={18} className="md:w-5 md:h-5" />
                    Send via Email
                  </button>

                  <button
                    onClick={() => setShowForm(false)}
                    className="w-full text-gray-600 hover:text-gray-800 py-2 text-sm md:text-base"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}