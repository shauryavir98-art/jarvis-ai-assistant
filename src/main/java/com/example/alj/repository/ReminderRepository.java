package com.example.alj.repository;

import com.example.alj.entity.Reminder;
import com.example.alj.entity.ReminderStatus;
import com.example.alj.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReminderRepository extends JpaRepository<Reminder, Long> {

    List<Reminder> findByUserOrderByReminderTimeDesc(User user);

    List<Reminder> findByUserAndStatusOrderByReminderTimeAsc(User user, ReminderStatus status);

    List<Reminder> findTop5ByUserAndStatusOrderByReminderTimeAsc(User user, ReminderStatus status);

    long countByUserAndStatus(User user, ReminderStatus status);

    long countByUser(User user);
}
