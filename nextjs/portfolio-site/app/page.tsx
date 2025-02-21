"use client";
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'; // For GitHub Flavored Markdown support
import rehypeRaw from 'rehype-raw'; // For HTML support in Markdown

export default function Home() {
  const [markdown, setMarkdown] = useState('');
  const [submittedContent, setSubmittedContent] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittedContent(markdown);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="flex justify-between items-center p-4 bg-gray-100 border-b">
        <div className="text-xl font-bold">Rahul</div>
        <div className="text-xl cursor-pointer">🔍</div>
      </nav>

      <main className="flex-1 p-8 flex flex-col items-center">
        <h1 className="text-3xl mb-8">Welcome to My Portfolio</h1>

        <div className="w-full max-w-2xl flex flex-col gap-6">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <textarea
              className="w-full p-4 border rounded-md resize-y"
              value={markdown}
              onChange={(e) => setMarkdown(e.target.value)}
              placeholder="Write your markdown here..."
              rows={10}
            />
            <button
              type="submit"
              className="self-start px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Submit
            </button>
          </form>

          {submittedContent && (
            <div className="p-4 border rounded-md w-full prose">
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
      </main>
    </div>
  );
}