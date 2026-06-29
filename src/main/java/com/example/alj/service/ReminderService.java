package com.example.alj.service;

import com.example.alj.dto.ReminderDto;
import com.example.alj.entity.Reminder;
import com.example.alj.entity.ReminderStatus;
import com.example.alj.entity.User;
import com.example.alj.repository.ReminderRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ReminderService {

    private final ReminderRepository reminderRepository;

    @Transactional
    public ReminderDto createReminder(ReminderDto dto, User user) {
        Reminder reminder = Reminder.builder()
                .title(dto.getTitle())
                .reminderTime(dto.getReminderTime())
                .status(ReminderStatus.PENDING)
                .user(user)
                .build();

        reminder = reminderRepository.save(reminder);
        return toDto(reminder);
    }

    public List<ReminderDto> getAllReminders(User user) {
        return reminderRepository.findByUserOrderByReminderTimeDesc(user)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    public List<ReminderDto> getPendingReminders(User user) {
        return reminderRepository.findByUserAndStatusOrderByReminderTimeAsc(user, ReminderStatus.PENDING)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    public List<ReminderDto> getUpcomingReminders(User user) {
        return reminderRepository.findTop5ByUserAndStatusOrderByReminderTimeAsc(user, ReminderStatus.PENDING)
                .stream()
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Transactional
    public ReminderDto updateStatus(Long id, String status, User user) {
        Reminder reminder = reminderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Reminder not found with id: " + id));

        if (!reminder.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("You do not have permission to modify this reminder");
        }

        reminder.setStatus(ReminderStatus.valueOf(status.toUpperCase()));
        reminder = reminderRepository.save(reminder);
        return toDto(reminder);
    }

    @Transactional
    public void deleteReminder(Long id, User user) {
        Reminder reminder = reminderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Reminder not found with id: " + id));

        if (!reminder.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("You do not have permission to delete this reminder");
        }

        reminderRepository.delete(reminder);
    }

    public long getTotalCount(User user) {
        return reminderRepository.countByUser(user);
    }

    public long getPendingCount(User user) {
        return reminderRepository.countByUserAndStatus(user, ReminderStatus.PENDING);
    }

    private ReminderDto toDto(Reminder reminder) {
        return ReminderDto.builder()
                .id(reminder.getId())
                .title(reminder.getTitle())
                .reminderTime(reminder.getReminderTime())
                .status(reminder.getStatus().name())
                .build();
    }
}
