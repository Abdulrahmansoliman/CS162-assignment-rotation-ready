// Page for displaying detailed information about a single item.
// Fetches item data from the backend and focuses on read-only presentation,
// including loading/error states and UI-only interactions (e.g. share link).

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getItemById } from '@/api/item';
import { verifyItem, getItemVerifications } from '@/api/verification';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card';
import { Button } from '@/shared/components/ui/button';
import { Spinner } from '@/shared/components/ui/spinner';
<<<<<<< HEAD
<<<<<<< HEAD
import { MapPin, Clock, User, CheckCircle, Tag, ArrowLeft, Share2, Navigation } from 'lucide-react';
=======
import { MapPin, Clock, User, CheckCircle, Tag, ArrowLeft, Share2, Bookmark, Navigation } from 'lucide-react';
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
=======
import { MapPin, Clock, User, CheckCircle, Tag, ArrowLeft, Share2, Navigation } from 'lucide-react';
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
import { colorSchemes, defaultScheme } from '@/lib/themes.js';
import '@/shared/styles/locale-theme.css';

export default function ItemDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [item, setItem] = useState(null);
  const [verifications, setVerifications] = useState([]);
  const [verifying, setVerifying] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
  const scheme = item && item.rotation_city ? (colorSchemes[item.rotation_city.name] || defaultScheme) : defaultScheme;

  const getLocaleClass = () => {
    if (!item?.rotation_city?.name) return '';
    const cityNameLower = item.rotation_city.name.toLowerCase();
    if (cityNameLower.includes('taipei')) return 'transition-green';
    if (cityNameLower.includes('seoul')) return 'transition-korea';
    if (cityNameLower.includes('buenos aires')) return 'transition-argentina';
    if (cityNameLower.includes('hyderabad')) return 'transition-india';
    if (cityNameLower.includes('berlin')) return 'transition-germany';
    return 'show-photo';
  };

  const getLocaleForCategoryColors = () => {
    if (!item?.rotation_city?.name) return 'usa';
    const cityNameLower = item.rotation_city.name.toLowerCase();
    if (cityNameLower.includes('taipei')) return 'china';
    if (cityNameLower.includes('seoul')) return 'korea';
    if (cityNameLower.includes('buenos aires')) return 'argentina';
    if (cityNameLower.includes('hyderabad')) return 'india';
    if (cityNameLower.includes('berlin')) return 'germany';
    return 'usa';
  };

  const localeCategoryPalettes = {
    usa: ["#002856", "#A50404", "#B8500C", "#F6DBAF", "#F6DBAF"],        
    china: ["#2c6e49", "#4c956c", "#ffc9b9", "#d68c45"],
    korea: ["#f9dbbd", "#ffa5ab", "#da627d", "#a53860", "#450920"],
    argentina: ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
    india: ["#cc5803", "#e2711d", "#ff9505", "#ffb627", "#ffc971"],
    germany: ["#003459", "#007ea7", "#00a8e8"],
  };

  const getCategoryColor = (index) => {
    const locale = getLocaleForCategoryColors();
    const palette = localeCategoryPalettes[locale] || localeCategoryPalettes['usa'];
    return palette[index % palette.length];
  };

  const getBackButtonColor = () => {
    const localeClass = getLocaleClass();
    const colorMap = {
      'show-photo': '#A50404',      // San Francisco - dark red
      'transition-green': '#1d9a5c',     // China - green
      'transition-korea': '#c60c30',     // Korea - red
      'transition-argentina': '#d9a300', // Argentina - gold
      'transition-india': '#ff9933',     // India - orange
      'transition-germany': '#7ab3e8'    // Germany - blue
    };
    return colorMap[localeClass] || '#A50404';
  };

<<<<<<< HEAD
=======
  const scheme = item && item.rotation_city ? colorSchemes[item.rotation_city.name] || defaultScheme : defaultScheme;
  
  const handleDirections = () => {
    if (item?.rotation_city?.res_hall_location && item?.location) {
      const origin = encodeURIComponent(item.rotation_city.res_hall_location);
      const destination = encodeURIComponent(item.location);
      const url = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}&travelmode=walking`;
      window.open(url, '_blank');
    }
  };
  
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
=======
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
  const handleShare = async () => {
    await navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getInitialsFromName = (fullName) => {
    if (!fullName) return "?";
    const parts = fullName.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return parts[0]?.substring(0, 2).toUpperCase() || "?";
  };

  const loadVerifications = async () => {
    try {
      const v = await getItemVerifications(id);
      setVerifications(v?.verifications || []);
    } catch {
      // Don't break the page if verifications fails
      setVerifications([]);
    }
  };

  const handleGoToUserProfile = () => {
    const userId = item?.added_by_user?.user_id;
    if (!userId) return;
    navigate(`/user/${userId}`);
  };

  useEffect(() => {
    const fetchItem = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getItemById(id);
        setItem(data);

        // fetch verifications after item loads
        await loadVerifications();
      } catch (err) {
        setError(err.message || 'Failed to load item details');
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchItem();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const handleVerify = async () => {
    try {
      setVerifying(true);
      await verifyItem(id);

      // optimistic count update (so UI updates immediately)
      setItem((prev) => ({
        ...prev,
        number_of_verifications: (prev?.number_of_verifications || 0) + 1,
      }));

      await loadVerifications();
    } catch (e) {
      alert("You already verified today (or an error occurred).");
    } finally {
      setVerifying(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <Spinner className="w-12 h-12" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
        <Card className="w-full max-w-md bg-slate-800/90 backdrop-blur-sm border-slate-700">
          <CardHeader>
            <CardTitle className="text-red-400">Error</CardTitle>
            <CardDescription className="text-slate-300">{error}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate(-1)} className="w-full">
              Go Back
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <Card className="w-full max-w-md bg-black backdrop-blur-sm border-slate-700">
          <CardHeader>
            <CardTitle className="text-slate-200">Item not found</CardTitle>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate(-1)} className="w-full">
              Go Back
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const firstInitial = item.added_by_user?.first_name?.[0] || '';
  const lastInitial = item.added_by_user?.last_name?.[0] || '';
  const profilePic = item.added_by_user?.profile_picture || null;

  return (
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
    <div style={{ paddingBottom: "2rem" }}>
      {/* Header with Item Title - Matching Main Page */}
      <div className={`locale-container ${getLocaleClass()}`} style={{ color: "white", padding: "3rem 2rem 2rem 2rem", position: "relative" }}>
        <div className={`locale-overlay absolute inset-0 ${getLocaleClass()}`}></div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", position: "relative", zIndex: 10, maxWidth: "1200px", margin: "0 auto" }}>
          <div style={{ flex: 1 }}>
            <h1 style={{ fontSize: "2.5rem", margin: 0, fontWeight: 300, letterSpacing: "1px", fontFamily: 'Fraunces, serif' }}>
              {item?.name || 'Item Details'}
            </h1>
            {item?.rotation_city && (
              <div style={{ margin: "0.5rem 0 0 0", display: "inline-block" }}>
                <span style={{ fontSize: "0.85rem", opacity: 0.9, background: "rgba(255, 255, 255, 0.2)", borderRadius: "20px", padding: "0.4rem 0.8rem", backdropFilter: "blur(10px)" }}>
                  {item.rotation_city.name}
                </span>
              </div>
            )}
<<<<<<< HEAD
=======
    <div className={`min-h-screen ${scheme.bg}`}>
      {/* Hero Section */}
      <div className={`relative ${scheme.heroBg} overflow-hidden`}>
        <div className={`absolute inset-0 ${scheme.overlay}`}></div>
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-30"></div>

        <div className="relative max-w-6xl mx-auto px-4 py-12">
          <Button
            onClick={() => navigate(-1)}
            variant="ghost"
            className="mb-6 text-white hover:bg-white/20 transition-all border border-white/25 rounded-lg"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>

          <div className="flex flex-col md:flex-row gap-8 items-start">
            <div className="flex-1">
              <button
                type="button"
                onClick={handleGoToUserProfile}
                className="inline-flex items-center gap-2 px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full mb-4 hover:bg-white/30 transition"
              >
                <div className="w-6 h-6 rounded-full bg-white/30 flex items-center justify-center overflow-hidden">
                  {profilePic ? (
                    <img
                      src={profilePic}
                      alt={item.added_by_user?.first_name || 'User'}
                      className="w-full h-full object-cover rounded-full"
                    />
                  ) : (
                    <span className="text-white font-semibold text-xs">
                      {firstInitial}{lastInitial}
                    </span>
                  )}
                </div>
                <span className="text-white text-sm font-medium">
                  Recommended by {item.added_by_user?.first_name || 'a fellow student'}
                </span>
              </button>

              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 leading-tight">
                {item.name}
              </h1>

              <div className="flex flex-wrap gap-4 mb-6">
                <div className="flex items-center gap-2 text-white/90">
                  <MapPin className="w-5 h-5" />
                  <span className="text-lg">{item.location}</span>
                </div>
                {item.walking_distance && (
                  <div className="flex items-center gap-2 text-white/90">
                    <Clock className="w-5 h-5" />
                    <span className="text-lg">{Math.round(item.walking_distance / 80)} min walk</span>
                  </div>
                )}
              </div>

              {item.categories && item.categories.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-6">
                  {item.categories.map((category) => (
                    <span
                      key={category.category_id}
                      className="px-4 py-2 bg-white/90 text-gray-900 rounded-lg text-sm font-semibold shadow-lg"
                    >
                      {category.name}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Right: Quick Stats Card */}
            <div className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-2xl min-w-[280px]">
              <div className="flex items-center justify-center gap-2 pb-4 border-b border-gray-200">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="text-lg font-semibold text-gray-900">
                  {item.number_of_verifications || 0} {(item.number_of_verifications || 0) === 1 ? 'Verification' : 'Verifications'}
                </span>
              </div>
              <div className="border-t border-gray-200 pt-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">City</span>
                  <span className="font-semibold text-gray-900">{item.rotation_city?.name || "—"}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Added</span>
                  <span className="font-semibold text-gray-900">
                    {item.created_at ? new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : "—"}
                  </span>
                </div>
              </div>

              <div className="mt-6 space-y-2">
                {item.rotation_city?.res_hall_location && (
                  <Button
                    className={`w-full ${scheme.heroBg} text-white hover:opacity-90 shadow-lg`}
                    onClick={handleDirections}
                  >
                    <Navigation className="w-4 h-4 mr-2" />
                    Get Directions
                  </Button>
                )}
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    className="flex-1"
                    onClick={handleShare}
                  >
                    <Share2 className="w-4 h-4 mr-2" />
                    {copied ? "Copied!" : "Share"}
                  </Button>
                </div>
              </div>
            </div>
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
=======
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
          </div>
          <button
            onClick={() => navigate(-1)}
            style={{
              width: "60px",
              height: "60px",
              borderRadius: "50%",
              border: "none",
              background: "white",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              flexShrink: 0,
              marginLeft: "2rem",
              transition: "all 0.3s ease",
              fontSize: "28px",
              color: getBackButtonColor()
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "scale(1.05)";
              e.currentTarget.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "scale(1)";
              e.currentTarget.style.boxShadow = "none";
            }}
          >
            ←
          </button>
        </div>
      </div>

      {/* Content Section - Like Main Page */}
      <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto", backgroundColor: "#f9fafb" }}>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Info Card */}
            <Card className={`${scheme.cardBg} ${scheme.border} shadow-md hover:shadow-lg transition-all duration-200 rounded-xl overflow-hidden`}>
              <CardHeader className="bg-gradient-to-r from-white to-gray-50 border-b border-gray-200">
                <CardTitle className="text-lg text-gray-900 font-bold">
                  Details
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-6 space-y-4">
                {item.location && (
                  <div className="flex items-start gap-4 pb-4 border-b border-gray-200 last:border-0">
                    <div className="flex-1">
                      <div className="text-xs uppercase tracking-wider text-gray-400 font-bold mb-1">Location</div>
                      <div className="text-gray-900 font-semibold text-base">{item.location}</div>
                    </div>
                  </div>
                )}
                {item.walking_distance !== null && item.walking_distance !== undefined && item.walking_distance > 0 && (
                  <div className="flex items-start gap-4 pb-4 border-b border-gray-200 last:border-0">
                    <Clock className="w-6 h-6 text-green-500 mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="text-xs uppercase tracking-wider text-gray-400 font-bold mb-1">Walking Distance</div>
                      <div className="text-gray-900 font-semibold text-base">{Math.round(item.walking_distance / 80)} min walk</div>
                      <div className="text-xs text-gray-500 mt-1">({item.walking_distance}m from campus)</div>
                    </div>
                  </div>
                )}
                {item.categories && item.categories.length > 0 && (
                  <div className="flex items-start gap-4">
                    <div className="flex-1">
                      <div className="text-xs uppercase tracking-wider text-gray-400 font-bold mb-3">Categories</div>
                      <div className="flex flex-wrap gap-2">
                        {item.categories.map((category) => (
                          <span
                            key={category.category_id}
                            className="px-3 py-1.5 text-white rounded-full text-xs font-semibold transition-all"
                            style={{
                              backgroundColor: getCategoryColor(category.category_id),
                              opacity: 0.9
                            }}
                          >
                            {category.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Details & Attributes */}
            {item.tags && item.tags.length > 0 && (
              <Card className={`${scheme.cardBg} ${scheme.border} shadow-md hover:shadow-lg transition-all duration-200 rounded-xl overflow-hidden`}>
                <CardHeader className="bg-gradient-to-r from-white to-gray-50 border-b border-gray-200">
                  <CardTitle className="text-lg text-gray-900 font-bold">
                    More information
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {item.tags.map((tag) => (
                      <div
                        key={tag.tag_id}
                        className={`${scheme.innerBg} rounded-lg p-4 flex items-center justify-between border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all`}
                      >
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900">{tag.name}</div>
                        </div>
                        <div className="ml-4">
                          {tag.value_type === 'boolean' ? (
                            <span className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                              tag.value
                                ? 'bg-green-100 text-green-700'
                                : 'bg-red-100 text-red-700'
                            }`}>
                              {tag.value ? '✓ Yes' : '✗ No'}
                            </span>
                          ) : (
                            <span className="text-gray-900 font-semibold text-sm bg-gray-100 px-3 py-1.5 rounded-lg">{tag.value}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Action Buttons */}
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {/* Share Location Button */}
              <button
                onClick={handleShare}
                style={{
                  width: "100%",
                  padding: "0.75rem 1rem",
                  borderRadius: "0.5rem",
                  border: "none",
                  background: "white",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "0.5rem",
                  cursor: "pointer",
                  transition: "all 0.3s ease",
                  color: "rgba(0, 0, 0, 0.7)",
                  fontSize: "0.9rem",
                  fontWeight: "600",
                  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)"
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)";
                  e.currentTarget.style.background = "#f9fafb";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = "0 2px 8px rgba(0, 0, 0, 0.1)";
                  e.currentTarget.style.background = "white";
                }}
                title={copied ? "Copied!" : "Share this item"}
              >
                <span>{copied ? "Copied" : "Share location"}</span>
                {copied ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  <Share2 className="w-5 h-5" />
                )}
              </button>
              
              {/* Get Directions Button */}
              <button
                onClick={() => {
                  if (item?.location) {
                    const mapsUrl = `https://www.google.com/maps/search/${encodeURIComponent(item.location)}`;
                    window.open(mapsUrl, '_blank');
                  }
                }}
                style={{
                  width: "100%",
                  padding: "0.75rem 1rem",
                  borderRadius: "0.5rem",
                  border: "none",
                  background: "white",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "0.5rem",
                  cursor: "pointer",
                  transition: "all 0.3s ease",
                  color: "rgba(0, 0, 0, 0.7)",
                  fontSize: "0.9rem",
                  fontWeight: "600",
                  boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)",
                  opacity: item?.location ? 1 : 0.5
                }}
                onMouseEnter={(e) => {
                  if (item?.location) {
                    e.currentTarget.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)";
                    e.currentTarget.style.background = "#f9fafb";
                  }
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = "0 2px 8px rgba(0, 0, 0, 0.1)";
                  e.currentTarget.style.background = "white";
                }}
                disabled={!item?.location}
                title="Get directions"
              >
                <span>Get directions</span>
                <Navigation className="w-5 h-5" />
              </button>
            </div>

            {/* Recommender Card */}
            {item.added_by_user && (
              <Card className={`${scheme.cardBg} ${scheme.border} shadow-md hover:shadow-lg transition-all duration-200 rounded-xl overflow-hidden`}>
                <CardHeader className="bg-gradient-to-r from-white to-gray-50 border-b border-gray-200">
                  <CardTitle className="text-base text-gray-900 font-bold">
                    Recommended by
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-6">
                  <button
                    type="button"
                    onClick={handleGoToUserProfile}
                    className="w-full text-left hover:opacity-80 transition-opacity"
                  >
                    <div className="flex items-start gap-4">
                      <div className="w-14 h-14 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center overflow-hidden flex-shrink-0 border-2 border-white shadow-md">
                        {profilePic ? (
                          <img
                            src={profilePic}
                            alt={`${item.added_by_user.first_name} ${item.added_by_user.last_name}`}
                            className="w-full h-full object-cover"
                          />
                        ) : (
                          <span className="text-gray-700 font-bold text-lg">
                            {firstInitial}{lastInitial}
                          </span>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900 text-lg hover:text-blue-600 transition-colors">
                          {item.added_by_user.first_name} {item.added_by_user.last_name}
                        </div>
                        <div className="text-sm text-gray-600 mt-0.5 line-clamp-1">
                          {item.added_by_user.email}
                        </div>
                        <div className="mt-2 text-xs text-gray-500 leading-relaxed">
                          Minerva student sharing local insights
                        </div>
                      </div>
                    </div>
                  </button>
                </CardContent>
              </Card>
            )}

            {/* Verified By Card */}
            <Card className={`${scheme.cardBg} ${scheme.border} shadow-md hover:shadow-lg transition-all duration-200 rounded-xl overflow-hidden`}>
              <CardHeader className="bg-gradient-to-r from-white to-gray-50 border-b border-gray-200">
                <CardTitle className="text-base text-gray-900 font-bold">
                  Verified by
                </CardTitle>
                <CardDescription className="text-gray-600 text-xs mt-1">
                  {verifications.length} {verifications.length === 1 ? 'person' : 'people'} verified
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6 space-y-3">
                {verifications.length === 0 ? (
                  <p className="text-sm text-gray-500">No verifications yet. Be the first!</p>
                ) : (
                  verifications.map((v) => (
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
                    <div key={v.verification_id} className="flex items-center gap-3 pb-2 border-b border-gray-100 last:border-0">
                      <div className="w-9 h-9 rounded-full flex items-center justify-center font-semibold text-sm flex-shrink-0 overflow-hidden border-2 border-gray-200">
                        {v.profile_picture ? (
                          <img
                            src={v.profile_picture}
                            alt={v.user_name}
                            className="w-full h-full object-cover"
                          />
                        ) : (
                          <div className="w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center text-blue-700">
                            {getInitialsFromName(v.user_name)}
                          </div>
<<<<<<< HEAD
=======
                    <div key={v.verification_id} className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center font-semibold text-gray-900 text-sm overflow-hidden">
                        {v.user_photo ? (
                          <img
                            src={v.user_photo}
                            alt={v.user_name || "Anonymous"}
                            className="w-full h-full object-cover rounded-full"
                          />
                        ) : (
                          <span>{getInitialsFromName(v.user_name)}</span>
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
=======
>>>>>>> a817a4c7c530ceb80354cc37ab7bc0f0ee90d2e1
                        )}
                      </div>
                      <div className="text-sm text-gray-900 font-medium truncate">
                        {v.user_name || "Anonymous"}
                      </div>
                    </div>
                  ))
                )}
              </CardContent>
            </Card>

          </div>
        </div>
      </div>
    </div>
  );
}



