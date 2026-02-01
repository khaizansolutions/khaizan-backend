'use client'
import { use, useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { ShoppingCart, MessageCircle, Heart, Share2, Star, Truck, Shield, RefreshCcw, ArrowLeft, ChevronDown, ChevronUp } from 'lucide-react'
import { useQuote } from '@/context/QuoteContext'
import { ProductDetailSkeleton } from '@/components/common/LoadingSkeleton'
import { getProductById, Product } from '@/data/products'

export default function ProductDetail({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params)
  const [loading, setLoading] = useState(true)
  const [product, setProduct] = useState<Product | null>(null)
  const [activeTab, setActiveTab] = useState('features')
  const [quantity, setQuantity] = useState(1)
  const { addToQuote } = useQuote()

  useEffect(() => {
    setTimeout(() => {
      const foundProduct = getProductById(parseInt(resolvedParams.id))
      setProduct(foundProduct || null)
      setLoading(false)
    }, 1000)
  }, [resolvedParams.id])

  if (loading) {
    return <ProductDetailSkeleton />
  }

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl md:text-4xl font-bold mb-4">Product Not Found</h1>
        <p className="text-gray-600 mb-8 text-sm md:text-base">The product you're looking for doesn't exist.</p>
        <Link href="/products">
          <button className="bg-primary text-white px-6 md:px-8 py-2 md:py-3 rounded-lg hover:bg-blue-700 transition">
            Browse All Products
          </button>
        </Link>
      </div>
    )
  }

  const handleAddToQuote = () => {
    addToQuote({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      category: product.category,
      quantity: quantity,
    })
    alert(`Added ${quantity} item(s) to quote!`)
  }

  const handleWhatsApp = () => {
    const message = `Hi, I'm interested in:\n\n*${product.name}*\nQuantity: ${quantity}\nPrice: AED ${product.price.toFixed(2)}\nSKU: ${product.sku}\n\nCould you provide more details?`
    const whatsappUrl = `https://wa.me/971445222261?text=${encodeURIComponent(message)}`
    window.open(whatsappUrl, '_blank')
  }

  const incrementQuantity = () => {
    if (quantity < product.stockCount) {
      setQuantity(quantity + 1)
    }
  }

  const decrementQuantity = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1)
    }
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Breadcrumb - Desktop Only */}
      <div className="hidden md:block bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Link href="/" className="hover:text-primary">Home</Link>
            <span>/</span>
            <Link href="/products" className="hover:text-primary">Products</Link>
            <span>/</span>
            <Link href={`/products?category=${product.category}`} className="hover:text-primary">
              {product.category}
            </Link>
            <span>/</span>
            <span className="text-gray-900 truncate">{product.name}</span>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-3 md:px-4 py-4 md:py-8">
        {/* Back Button */}
        <Link 
          href="/products" 
          className="inline-flex items-center gap-2 text-primary hover:underline mb-4 md:mb-6 text-sm md:text-base"
        >
          <ArrowLeft size={18} className="md:w-5 md:h-5" />
          Back to Products
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-12 bg-white rounded-lg shadow-lg p-4 md:p-8">
          {/* Left Column - Images */}
          <div>
            {/* Main Image */}
            <div className="relative h-64 sm:h-80 md:h-96 lg:h-[500px] bg-gray-100 rounded-lg overflow-hidden mb-3 md:mb-4">
              <Image
                src={product.image}
                alt={product.name}
                fill
                className="object-cover"
                priority
              />
              {product.discount && product.discount > 0 && (
                <div className="absolute top-2 md:top-4 left-2 md:left-4 bg-red-500 text-white px-2 md:px-3 py-1 rounded-full font-bold text-xs md:text-sm">
                  -{product.discount}%
                </div>
              )}
            </div>

            {/* Thumbnail Images */}
            {product.images && product.images.length > 0 && (
              <div className="grid grid-cols-4 gap-2 md:gap-4">
                {product.images.map((img: string, index: number) => (
                  <div 
                    key={index} 
                    className="relative h-16 sm:h-20 md:h-24 bg-gray-100 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-primary transition"
                  >
                    <Image
                      src={img}
                      alt={`${product.name} - Image ${index + 1}`}
                      fill
                      className="object-cover"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Right Column - Product Info */}
          <div>
            {/* Brand & SKU */}
            <div className="flex items-center gap-2 md:gap-4 mb-2 text-xs md:text-sm text-gray-500">
              <span>Brand: {product.brand}</span>
              <span>|</span>
              <span>SKU: {product.sku}</span>
            </div>

            {/* Product Name */}
            <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold mb-3 md:mb-4 leading-tight">
              {product.name}
            </h1>

            {/* Rating & Reviews */}
            <div className="flex items-center gap-2 md:gap-4 mb-3 md:mb-4 text-sm md:text-base">
              <div className="flex items-center gap-1">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    size={16}
                    className={`md:w-5 md:h-5 ${i < Math.floor(product.rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}`}
                  />
                ))}
              </div>
              <span className="text-gray-600 text-xs md:text-sm">{product.rating} / 5</span>
              <span className="text-primary hover:underline cursor-pointer text-xs md:text-sm">
                ({product.reviews} reviews)
              </span>
            </div>

            {/* Price */}
            <div className="mb-4 md:mb-6">
              <div className="flex items-center gap-3 md:gap-4">
                <span className="text-2xl sm:text-3xl md:text-4xl font-bold text-primary">
                  AED {product.price.toFixed(2)}
                </span>
                {product.originalPrice && (
                  <span className="text-lg sm:text-xl md:text-2xl text-gray-400 line-through">
                    AED {product.originalPrice.toFixed(2)}
                  </span>
                )}
              </div>
              {product.originalPrice && (
                <p className="text-xs md:text-sm text-green-600 mt-1">
                  Save AED {(product.originalPrice - product.price).toFixed(2)}
                </p>
              )}
            </div>

            {/* Stock Status */}
            {product.inStock ? (
              <div className="flex items-center gap-2 mb-4 md:mb-6">
                <span className="inline-block bg-green-100 text-green-800 px-2 md:px-3 py-1 rounded-full text-xs md:text-sm font-semibold">
                  In Stock
                </span>
                <span className="text-gray-600 text-xs md:text-sm">({product.stockCount} units available)</span>
              </div>
            ) : (
              <span className="inline-block bg-red-100 text-red-800 px-2 md:px-3 py-1 rounded-full text-xs md:text-sm font-semibold mb-4 md:mb-6">
                Out of Stock
              </span>
            )}

            {/* Description */}
            <p className="text-gray-700 mb-4 md:mb-6 leading-relaxed text-sm md:text-base">
              {product.description}
            </p>

            {/* Quantity Selector */}
            <div className="mb-4 md:mb-6">
              <label className="block text-xs md:text-sm font-semibold mb-2">Quantity:</label>
              <div className="flex items-center gap-3 md:gap-4">
                <div className="flex items-center border-2 border-gray-300 rounded-lg">
                  <button 
                    onClick={decrementQuantity}
                    className="px-3 md:px-4 py-2 hover:bg-gray-100 transition text-lg md:text-xl"
                  >
                    -
                  </button>
                  <input 
                    type="number" 
                    value={quantity}
                    onChange={(e) => {
                      const val = parseInt(e.target.value)
                      if (val >= 1 && val <= product.stockCount) {
                        setQuantity(val)
                      }
                    }}
                    min={1}
                    max={product.stockCount}
                    className="w-12 md:w-16 text-center border-x-2 border-gray-300 py-2 focus:outline-none text-sm md:text-base"
                  />
                  <button 
                    onClick={incrementQuantity}
                    className="px-3 md:px-4 py-2 hover:bg-gray-100 transition text-lg md:text-xl"
                  >
                    +
                  </button>
                </div>
                <span className="text-xs md:text-sm text-gray-600">Max: {product.stockCount} units</span>
              </div>
            </div>

            {/* Action Buttons - Mobile Stacked */}
            <div className="flex flex-col md:flex-row gap-2 md:gap-4 mb-6 md:mb-8">
              <button 
                onClick={handleAddToQuote}
                className="flex-1 bg-primary text-white py-3 md:py-4 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 text-sm md:text-lg font-semibold"
              >
                <ShoppingCart size={20} className="md:w-6 md:h-6" />
                Add to Quote
              </button>
              <button 
                onClick={handleWhatsApp}
                className="flex-1 md:flex-initial bg-green-500 text-white px-4 md:px-6 py-3 md:py-4 rounded-lg hover:bg-green-600 transition flex items-center justify-center gap-2 text-sm md:text-base"
              >
                <MessageCircle size={20} className="md:w-6 md:h-6" />
                WhatsApp
              </button>
              <button className="md:block hidden bg-gray-200 text-gray-700 p-4 rounded-lg hover:bg-gray-300 transition">
                <Heart size={24} />
              </button>
              <button className="md:block hidden bg-gray-200 text-gray-700 p-4 rounded-lg hover:bg-gray-300 transition">
                <Share2 size={24} />
              </button>
            </div>

            {/* Features Grid - Responsive */}
            <div className="grid grid-cols-3 gap-2 md:gap-4 mb-6 md:mb-8 p-3 md:p-6 bg-gray-50 rounded-lg">
              <div className="text-center">
                <Truck className="mx-auto mb-1 md:mb-2 text-primary" size={24} />
                <p className="text-[10px] sm:text-xs md:text-sm font-semibold">Free Delivery</p>
                <p className="text-[8px] sm:text-[10px] md:text-xs text-gray-600">Over AED 300</p>
              </div>
              <div className="text-center">
                <Shield className="mx-auto mb-1 md:mb-2 text-primary" size={24} />
                <p className="text-[10px] sm:text-xs md:text-sm font-semibold">{product.specifications.Warranty || '1 Year'}</p>
                <p className="text-[8px] sm:text-[10px] md:text-xs text-gray-600">Warranty</p>
              </div>
              <div className="text-center">
                <RefreshCcw className="mx-auto mb-1 md:mb-2 text-primary" size={24} />
                <p className="text-[10px] sm:text-xs md:text-sm font-semibold">Easy Returns</p>
                <p className="text-[8px] sm:text-[10px] md:text-xs text-gray-600">30-day policy</p>
              </div>
            </div>

            {/* Shipping Info - Desktop Only */}
            <div className="hidden md:block border-t pt-6">
              <h3 className="font-bold text-lg mb-3">Delivery Information</h3>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span>Free delivery on orders over AED 300</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span>Express delivery available (1-2 days) - AED 50</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">✓</span>
                  <span>Standard delivery: 2-3 business days</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Product Details Tabs */}
        <div className="mt-6 md:mt-12 bg-white rounded-lg shadow-lg p-4 md:p-8">
          {/* Tabs Header */}
          <div className="border-b mb-4 md:mb-6 overflow-x-auto">
            <div className="flex gap-4 md:gap-8 min-w-max">
              <button
                onClick={() => setActiveTab('features')}
                className={`pb-3 md:pb-4 text-sm md:text-base whitespace-nowrap ${
                  activeTab === 'features'
                    ? 'border-b-2 border-primary text-primary font-semibold'
                    : 'text-gray-600 hover:text-primary'
                }`}
              >
                Features
              </button>
              <button
                onClick={() => setActiveTab('specifications')}
                className={`pb-3 md:pb-4 text-sm md:text-base whitespace-nowrap ${
                  activeTab === 'specifications'
                    ? 'border-b-2 border-primary text-primary font-semibold'
                    : 'text-gray-600 hover:text-primary'
                }`}
              >
                Specifications
              </button>
              <button
                onClick={() => setActiveTab('reviews')}
                className={`pb-3 md:pb-4 text-sm md:text-base whitespace-nowrap ${
                  activeTab === 'reviews'
                    ? 'border-b-2 border-primary text-primary font-semibold'
                    : 'text-gray-600 hover:text-primary'
                }`}
              >
                Reviews ({product.reviews})
              </button>
            </div>
          </div>

          {/* Features Tab */}
          {activeTab === 'features' && (
            <div>
              <h3 className="text-lg md:text-2xl font-bold mb-4 md:mb-6">Key Features</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
                {product.features.map((feature: string, index: number) => (
                  <div key={index} className="flex items-start gap-2 md:gap-3 p-3 md:p-4 bg-gray-50 rounded-lg">
                    <span className="text-primary mt-1">✓</span>
                    <span className="text-gray-700 text-sm md:text-base">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Specifications Tab */}
          {activeTab === 'specifications' && (
            <div>
              <h3 className="text-lg md:text-2xl font-bold mb-4 md:mb-6">Technical Specifications</h3>
              <div className="space-y-3 md:space-y-4">
                {Object.entries(product.specifications).map(([key, value]) => (
                  <div key={key} className="flex justify-between p-3 md:p-4 border-b">
                    <span className="font-semibold text-gray-700 text-sm md:text-base">{key}:</span>
                    <span className="text-gray-600 text-sm md:text-base text-right">{value as string}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Reviews Tab */}
          {activeTab === 'reviews' && (
            <div className="text-center py-8 md:py-12">
              <p className="text-gray-500 text-sm md:text-base">Reviews coming soon...</p>
            </div>
          )}
        </div>

        {/* Delivery Info - Mobile Only */}
        <div className="md:hidden mt-6 bg-white rounded-lg shadow-lg p-4">
          <h3 className="font-bold text-base mb-3">Delivery Information</h3>
          <ul className="space-y-2 text-gray-700 text-sm">
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Free delivery on orders over AED 300</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Express delivery (1-2 days) - AED 50</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 mt-1">✓</span>
              <span>Standard delivery: 2-3 business days</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}