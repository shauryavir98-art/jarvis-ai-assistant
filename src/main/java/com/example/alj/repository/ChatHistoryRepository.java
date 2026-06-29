package com.example.alj.repository;

import com.example.alj.entity.ChatHistory;
import com.example.alj.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatHistoryRepository extends JpaRepository<ChatHistory, Long> {

    List<ChatHistory> findByUserOrderByTimestampDesc(User user);

    List<ChatHistory> findTop10ByUserOrderByTimestampDesc(User user);

    long countByUser(User user);
}
