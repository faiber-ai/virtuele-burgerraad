import { useState, useEffect } from "react";
import "./Sidebar.css";

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>Virtuele Burgerraad</h1>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + Nieuw Wetsvoorstel
        </button>
      </div>

      <div className="conversation-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">Nog geen analyses</div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${
                conv.id === currentConversationId ? "active" : ""
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-title">
                {conv.title || "Nieuwe Analyse"}
              </div>
              <div className="conversation-meta">
                {conv.message_count} reacties
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
