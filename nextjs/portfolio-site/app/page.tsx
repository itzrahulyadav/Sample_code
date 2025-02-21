"use client";
import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

export default function Home() {
  const [markdown, setMarkdown] = useState('');
  const [submittedContent, setSubmittedContent] = useState('');
  const [activeTab, setActiveTab] = useState<'blogs' | 'markdown'>('blogs');
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Toggle dark mode and save preference to localStorage
  const toggleDarkMode = () => {
    setIsDarkMode((prev) => {
      const newMode = !prev;
      localStorage.setItem('darkMode', newMode.toString());
      return newMode;
    });
  };

  // Check for saved dark mode preference on mount
  useEffect(() => {
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'true') {
      setIsDarkMode(true);
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittedContent(markdown);
  };

  const blogs = [
    { id: 1, title: "My First Blog", excerpt: "This is my first blog post..." },
    { id: 2, title: "Learning React", excerpt: "React is awesome..." },
    { id: 3, title: "Next.js Tips", excerpt: "Best practices for Next.js..." },
  ];

  return (
    <div className={`min-h-screen flex flex-col ${isDarkMode ? 'dark' : ''}`}>
      <nav className="flex items-center p-4 bg-gray-100 dark:bg-gray-800 border-b dark:border-gray-700">
        <div className="text-xl font-bold mr-8 text-gray-900 dark:text-white">Rahul</div>
        <div className="flex gap-4">
          <button
            className={`px-3 py-1 rounded-md ${
              activeTab === 'blogs'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-600 dark:text-gray-200'
            }`}
            onClick={() => setActiveTab('blogs')}
          >
            Blogs
          </button>
          <button
            className={`px-3 py-1 rounded-md ${
              activeTab === 'markdown'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-600 dark:text-gray-200'
            }`}
            onClick={() => setActiveTab('markdown')}
          >
            Markdown
          </button>
        </div>
        <div className="flex-1" />
        <button
          onClick={toggleDarkMode}
          className="text-xl p-1 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700"
          aria-label="Toggle dark mode"
        >
          {isDarkMode ? '☀️' : '🌙'}
        </button>
      </nav>

      <main className="flex-1 p-8 flex flex-col items-center bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
        <h1 className="text-3xl mb-8">Welcome to My Portfolio</h1>

        {activeTab === 'blogs' ? (
          <div className="w-full max-w-2xl flex flex-col gap-6">
            <h2 className="text-2xl mb-4">My Blogs</h2>
            {blogs.map((blog) => (
              <div
                key={blog.id}
                className="p-4 border rounded-md bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700"
              >
                <h3 className="text-xl font-semibold">{blog.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{blog.excerpt}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="w-full max-w-2xl flex flex-col gap-6">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <textarea
                className="w-full p-4 border rounded-md resize-y bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600"
                value={markdown}
                onChange={(e) => setMarkdown(e.target.value)}
                placeholder="Write your markdown here..."
                rows={10}
              />
              <button
                type="submit"
                className="self-start px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 dark:hover:bg-blue-500"
              >
                Submit
              </button>
            </form>

            {submittedContent && (
              <div className="p-4 border rounded-md w-full prose dark:prose-invert bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                <h2 className="text-xl mb-2">Rendered Content:</h2>
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                  components={{
                    img: ({ node, ...props }) => (
                      <img
                        style={{ float: props.align as any, margin: '0 0 1rem 1rem' }}
                        {...props}
                      />
                    ),
                  }}
                >
                  {submittedContent}
                </ReactMarkdown>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}